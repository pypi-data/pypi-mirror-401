# Original Prompt - 原始prompt

```
使用create-skill工具来创建skill，同时md尽量使用中文，文件名用英文，内容尽量用中文

1. 输入了几个文件，对应的是job的plan和执行统计信息，plan是指包括执行计划、dag图等，执行统计信息是runtime跑的数据量和执行时间等；
2. 输入的文件分别是job_profile.json是执行器跑的时间和数据量统计；plan.json则是执行计划，包括dag图，两者需要结合起来，如hashjoin，从job_profile.json不知道是hash-hash shuffle hash join还是broadcast hash join等；
3. 初始化一些主要信息，
    3.1 分类sql。从plan.json找出cz.sql.text是不是 refresh命令，如果是，则按照分类sql来找出需要优化的点；
    3.2 版本信息；plan.json可以获取版本(build_info里记录了，如，GitBranch:release-v1.2等信息），但版本不要暴露给结论，告诉你版本主要是后续会许升级到不同版本可能需要不同flag；
    3.3 vc信息；同时可以查看cz.inner.is.ap.vc是不是ap，如果为0，则不是ap模式，表示是gp模式，如果为1，则为ap模式，后续优化也会区分是ap还是GP；
    3.4 setting，plan.json记录了所有已经设置的flag，提示你如果已经有了，就不要再给建议了（不要在结论中提这些flag）
    3.5 执行计划，plan.json中的dml->stages里记录了所有dag执行的stage信息，同时对应着job_profile.json那些stage；
    3.6 统计所有operator耗时，以及在其stage的占比和整个sql占比，目的是为了后续做一些优化时，可以反复利用这些统计结果
    3.7 根据上面初始化信息得到的场景来选择后续使用的分析和优化策略
        增量计算job的分析和优化
        compaction job分析
        gpjob分析
        apjob分析
        等其他各种分类
4. 增量计算refresh sql优化，即增量相关的sql优化
  增量job任务优化分两大块，一种是从运行的stage/operator算子级别优化，一种是优化状态表
  4.1 增量stage/operator级别优化
    4.1.1 增量refresh还是全量refresh;可以从plan.json找到refresh的table名字，如果plan中refresh table的tablesink算子是OVERWRITE，但是不是写delta tablesink(plan.json中是找到tablesink算子，然后在table/path对应的字段找，可能是3元组，也可能是4元组，4元组，则一般最后一个是__delta__，表示写入delta文件的tablesink)，如果不是写delta tablesink则表示是全量(即overwrite sink的不是delta，且overwrite=true则表示是全量），否则是增量，同时忽略一些中间表，目前是通过名字带有__incr__这种pattern，表示的是中间状态，则这些暂时可以忽略，即不要找错了refresh的table名字；
    4.1.2 单dop aggregate stage优化；如果stage是dop=1（可以从job_profile.json里找），如果stage里包含了Hashaggregate的Final/Complete状态（可以从相应plan.json找），并且是计算类似MULTI_RANGE_COLLECT,_DF_BF_COLLECT这些聚集函数，耗时较长，则可以给出走3阶段建议，需要设置set cz.optimizer.incremental.df.three.phase.agg.enable=true;即这个stage优化建议是设置该参数,如果已经配置了该参数，可能aggregete使用了one pass，即complete phase，则可以加上 set cz.optimizer.enable.one.pass.agg=false;来优化，同时如果还是耗时较长，没有生成3阶段，看下aggregate上的bits是多少，如果大于等于536870912，小于1073741824，则可以设置 set cz.optimizer.df.three.phase.agg.bf.width.threshold=某个值，即bits大小，因为默认该阙值是1073741824(1.2版本以及1.2以下版本是这个，1.2以上默认值是536870912)，小于这个则不会生成3阶段，如果bits小于536870912，建议不要修改该参数；如果有类似final stage还是很慢，麻烦看下它上游stage，是不是没有走aggregate的P2，这样也会导致final agg很慢，如果是同样给出再看看没有开启3阶段，以及bits是不是比1073741824小，则需要调整；请同时看是否开启3阶段以及bits大小是否符合，否则仅仅开启3阶段还是无法达到预期；额外条件，如耗时，耗时比较多
        即优化条件：
        aggregate是Final或Complete状态，且上游不是P2状态，即没有开始3阶段aggregate
        耗时超过12s以上或者战总体15%以上
        dop=1
        agg有指定agg function
        如果未打开，则可以加上3阶段优化flag set cz.optimizer.incremental.df.three.phase.agg.enable=true;,如果已经有cz.optimizer.df.enable.three.phase.agg=true，则也不需要单独设置打开3阶段flag功能；
        但，如果不是3阶段需要检查bits是否满足，不满足需要额外加width threshold大小
    4.1.2 hash join优化；如果stage且耗时较长，如果stage里有join，且join占比比较多，可以看看是不是join的算法是hash-hash算法还是broadcast算法，统计信息可以从job_profile.json找，使用了什么算法，可以从plan.json找，一般来说，如果是broadcast，且shuffle量超大，则可以考虑禁止broadcast hash join，则给出优化建议是set cz.optimizer.enable.broadcast.hash.join=false;
    4.1.3 stage包含tablesink算子优化；我们stage的dop是通过累加得到，如果stage包好了tablesink算子，但是dop与上游不太一致，如果该stage耗时比较长，dop又与上游dop差异较大，则可能是由于会根据table的目标文件大小自动调整了dop，则给出set cz.sql.enable.dag.auto.adaptive.split.size=false;，该参数目的是不根据table的目标文件大小来自动调整dop;如果在这种场景下，stage里没有tablesink算子不要加该参数，即dop小并不是由于需要根据table目标文件大小来调整；同时建议看看每个stage的taskCount，如果其上游dop和自己相差不大，建议不要设置cz.sql.enable.dag.auto.adaptive.split.size，即下游stage一般不会超过上游dop,在不超过情况下不需要设置；
        即，优化条件
        stage包含tablesink算子
        dop与上游差异大
        dop如果与上游dop差不多（即计算依赖stage的
        task count)，则不需要额外设置cz.sql.enable.dag.auto.adaptive.split.size=false，即不需要根据此情况调整dop
        stage的dop大于上游stage的dop，则也不需要调整该参数，即下游dop都已经大于了上游，为啥还要调
    4.1.4 最大dop优化提示；我们dag这边限制了map的最大dop=4096，reduce最大dop=2048，所以碰到类似这种dop可以认为不是dop有问题，除非你有足够信服的理由，或者主动调整过这些dop，如cz.optimizer.mapper.stage.max.dop,cz.optimizer.reducer.stage.max.dop这些对应的flag;
    4.1.5 spillingBytes优化；关于spillingBytes分析，请按照算子级别来分析支持，一般有几种情况，一种是stage级别的总spill大小，还有一种是operator级别，可以相关spill stats看到有opId的，所以请根据这些级别来分析；如果是shuffle write的spill可能可以忽略；
    4.1.6 请你给出其他我未发现的问题，这里我发现你完全没理解，即不给任何分析，这里可以对所有stage看看时间耗时，对于那些比较慢的，可以主动分析为什么慢，如operator慢？还是其他等原因，希望你可以更smark点
  4.2 状态表优化
    4.2.0 如果给的prompt中没有提到使用状态优化，则不需要来使用下面优化原则来优化
    4.2.1 看看当前的job是否是增量刷新的job，即4.1.1提到的如何判断是增量还是全量
    4.2.2 如果job非增量刷新，请设置这些flag（
        set cz.optimizer.explain.incremental.plan=true;
        set cz.optimizer.print.non.incremental.reason=true;
        set cz.optimizer.print.non.incremental.reason_msg_max_length=100000;
        set cz.optimizer.incremental.force.incremental=true;
        ）后执行explain refresh...的命令以进一步查看问题成因
    4.2.3 当前任务执行速度不符合预期，请看看任务中是否包含 row number=1的pattern，如果包含请看看输入表是否是append-only的，你可以通过scan中是否包含__incremental_delete列来推断。如果是append-only但是window没有基于rn=1的结果继续计算，请设置以下flag继续尝试cz.optimizer.incremental.window.sd.to.sd.rule.enable=false; 如果任务退化成全量刷新了，则回到步骤2继续分析原因。如果是append-only的输入表，我希望你能检查table是否具备以下property：incr.append.only.table=true 或者 job是否具备 cz.optimizer.incremental.append.only.tables='xxx'，如果没有请提醒用户添加上
    4.2.4 基于我教给你的3的方法，看看当前query中是否还包含append-only的scan，如果包含，根据你的经验预判一下当前是否使用的算法并非最优的
    4.2.5 看看当前的任务是否包含增量临时状态表，如果不包含，可以设置cz.optimizer.incremental.enable.state.table=true;来开启。但是在开启之前，我希望你根据经验判断一下当前是否值得存储中间状态，你可以从以下几个方面进行判断：1.是否需要状态（可以参考流计算的带状态计算的定义），2.状态表是否过大（请根据当前看到的每一步的stats信息和输入表的增量数据大小进行合理判断）
    4.2.6 看看当前任务中aggregate的计算是否利用上了之前的计算结果（对于SUM，COUNT希望无论如何都尽量使用之前的结果，对于MIN，MAX希望在append-only的情况下尽量使用之前的结果），如果发现没用上，请根据5我教会你的方法看看是否存在状态，如果状态存在，请根据3教会你的方法看看是否有append-only的输入，如果是append-only但是缺少系统hint的，请补充上hint
    4.2.7 占比时间长calc可以存状态，如，calc占整体stage超过30%，同时整个stage在整体耗时占比10%以上,如果发现这类calc，可以看calc是不是有比较占比高的function计算，特别是udf(即用户自定义function)则可以通过set cz.optimizer.incremental.create.rule.based.table.on.heavy.calc=true;进行优化

5. compaction优化，TODO
6. gp job任务优化，TODO
7. ap job任务优化，TODO
8. 不要给没有提示的参数，即有些你给的flag是凭空说的;只在发现实际问题时才建议参数；其他的请单独列出，但是不要给什么强烈建议这种重跑，交给用户自己决定；
9. 可以将脚本按照不同sql分类来进行拆开，后续便于管理，即要考虑后续skill如何迭代；构建脚本尽量以不同场景来构建，方便扩展，如增量是一类，compaciton是一类等等;
   脚本命名不要和数字结合，容易导致prompt变了，但脚本数字和prompt对应不上问题
10. 脚本和md里不要出现v3，规则3这种带有版本或者数字第几章的东西，后续无法维护
```