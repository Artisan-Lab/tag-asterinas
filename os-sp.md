`Prior(f, g)` means `f` happens before the first appearance of `g` 


`Global` means the condition should be met in a global view/context



| ID  | Primitive SP | Meaning | Usage | Example API |
|---|---|---|---|---|
||CallOnce|CallCnt(Self)=1|Global|mm::frame::allocator::init_early_allocator|
||Fulfilled(f)|prior(f1, Self)| Precond | mm::frame::allocator::init_early_allocator|
||Unfulfilled(f)|prior(Self, f)| Precond | cpu::init_on_bsp|
||ValidNum(n)|n = num(hardware)| Precond | cpu::init_num_cpus |
||Unmodified(lo, hi)|∀vaddr∈(lo, hi), !prior(write(vaddr), Self)| Precond| copy_bsp_for_ap |
|??|ValidCpuId(id)|if Unfulfilled(Boot_end) then unique(id)| Precond | cpu::set_this_cpu_id|