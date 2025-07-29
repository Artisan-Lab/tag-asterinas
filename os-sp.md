# Asterinas SP

### Execution Sequence

safety::precond::PostToFunc(func, …)

safety::precond::NotPostToFunc(func, …)

safety::postcond::PriorToFunc(func, …)

safety::postcond::NotPriorToFunc(func, …)

safety::global::CallOnce(tag)

safety::global::Context(Tag) Tag ⇒ (start func, end func)

### Value

safety::precond::Eq/Le/Gt(a, b)

safety::precond::Align(a, val)

### Valid

safety::precond::ValidInstance(Constructor(val)) ⇒ 需要对类进行定制化

> 例如Slot(addr) ⇒ be a free slot in a [Slab], or  be a free slot in a [Segment].
> 

safety::precond::ValidPAddr(paddr) ⇒ 合法的物理内存地址

safety::precond::ValidIndex(src, idx) ⇒ ptr

safety::precond::ValidLevel(val, level)⇒ PTE或Cursor

safety::precond::ValidAccess(vaddr, KERNEL/USER/ANY, READ(len)/WRITE(len)/ANY(len)) ⇒ 内存空间

### Reference

safety::postcond::MutExclusive(val)

safety::global::MutExclusive(val)

safety::precond::RefHeld/RefUnheld(val) ⇒ 更强调是一种状态

safety::precond::Forgotten(val) ⇒ into_raw, ManuallyDrop, core::mem::forget

safety::postcond::NotOutLive(a,  b)

### Ownership

safey::postcond::Owned(val, owned)

### MISC

safety::precond::FrameUntrack ⇒ track的定义不明确

safety::postcond::KernalMemorySafe ⇒ unsafe的表现不明确

safety::postcond::Unaltered(AVAIL1) ⇒ AVAIL1作为一个标志位和参数的权属关系没有普适性

safety::precond::LockHeld ⇒ “逻辑上持有锁”很不清晰

safety::precond::SameAs

### MACROS

RETURN_VALUE: means the return value of the function