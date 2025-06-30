- #[safety::precond::SameAs(AtomicUsize::from_ptr)]

引用类

- #safety::postcond::MutExclusive(var)] 要求可变引用是独占的

- #safety::global::MutExclusive(var)]

上下文类

- #[safety::global::CallOnce]

- #[safety::global::TaggedCallOnce(Tag)] Tag：可以作为唯一性的Tag，例如参数的值等等

- #[safety::global::Context(Tag)] Tag应该是一个由函数指定的属性，例如Begin(BSP), Begin(AP)

- #[safety::precond::Initialized(var)]

- #[safety::precond::PostToFunc(var, func, args, …)] var可以是NULL或变量，表示返回值的去向

- #[safety::postcond::PriorToFunc(func, args, …)] args可以是Parameter/ReturnValue/Instance(Type)/通配符*

- #[safety::precond::NotPostToFunc(func)]
- #[safety::postcond::NotPriorToFunc(func)]

数值类

- #[safety::precond::Equal(a, b)]

- #[safety::precond::Le(a, b)]

- #[safety::precond::Align(var, val)]

一些特有的：

Frame

- #[safety::precond::ValidFrame(addr)]

- #[safety::precond::FrameRefHeld(addr)]

- #[safety::precond::FrameForgotten(addr)] = PostToFunc(into_raw/manuallydrop/core::mem::forget)

- #[safety::precond::SlotFrameRefHeld(slot)]

- #[safety::precond::FrameUntracked(addr/range)] = ? 在此之前不存在对这些物理页的mapping操作？

Segment

- #[safety::precond::RangeSegmentForgotten(range)] = PostToFunc(into_raw/manuallydrop/core::mem::forget)

Slot

- #[safety::precond::ValidSlot(addr)] 要求addr是slab或segment里的slot

Cursor

- #[safety::precond::SubtreeLocked(sub_tree)]
- #[safety::precond::SubtreeGuardForgotten(sub_tree)]

PageTableGuard

- #[safety::precond::PteIndexBounded(guard, idx)]

- #[safety::precond::PteLevelChild(guard, pte)]

- #[safety::postcond::PteOwned(guard, pte)]

- #[safety::precond::PteLevelMatch]

ChildRef

- #[safety::precond::ChildRefOutLive(pte)]

- #[safety::precond::NoChildRef(pte)]

PagTableNode

- #[safety::precond::LockHeld]  已持有pagetablenode的锁

- #[safety::precond::ProperMapping()]

PageTable

- #[safety::precond::NonBootPTActivated] = PostToFunc(activate/first_activate…)

- #[safety::precond::ValidKernelMapping(from)]

- #[safety::precond::Uncoppied(..)]

safety::precond::ProtectMemorySafe

- #[safety::precond::ValidReadLen(src, len)]
- #[safety::precond::ValidWriteLen(dst, len)]

- #[safety::precond::UserSpaceLen(dst, len)]

问题

- frame
    - Frame/UniqueFrame::from_raw的unsafe注释写的不严谨，除了into_raw还有manually drop等
    - frame_ref 有一个函数不方便完成注释
- kspace
    - mod中缺少注释
- paget_table
    - cursor
        - mod中map的safety过于抽象，是用一整个property来表示性质还是拆分开来？
    - node
        - mod中first_activate缺少safety注释
        - child中from_pte的要求没有履行，源数据并不是来自into_pte
    - unsafe trait暂时未处理