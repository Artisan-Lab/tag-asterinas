### Summary of Primitive SPs

| ID  | Primitive SP | Meaning | Usage | Example API |
|---|---|---|---|---|
|I.1|PostToFunc(func)|$\textsf{P} Call(func)$|Precond| |
|I.2|NotPostToFunc(func)|$\neg \textsf{P} Call(func)$|Precond| |
|I.3|NotPriorToFunc(func)|$\neg \Box(Call(func))$|Hazard| |
|I.4|CallOnce(scope)|$\textsf{F} Call(self) \wedge \Box(Call(self)\to\Box\neg Call(self))$|Hazard||
|I.5|Context(after, before)|Called between `after` and `before`| Hazard||
|II.1|Eq(lhs, rhs)|$lhs == rhs$| Precond||
|II.2|Ne(lhs, rhs)|$lhs != rhs$| Precond||
|II.3|Ge(lhs, rhs)|$lhs >= rhs$| Precond||
|III.1|Valid(val)|`val` should be valid|Precond||
|III.2|ValidFor(val, cond)|`val` should be valid for doing sth|Precond||
|IV.1|RefHeld(val)|$\exist ref(val)$|Precond||
|IV.2|RefUnheld(val)|$\neg \exist ref(val)$|Precond||
|IV.3|RefForgotten(val)|$\Box(Call_{self}(val) \to\textsf{P} Call(func_{forget}) \wedge (val=result))$|Precond||
|V.1|UserSpace(start, end)|$(start..end) \in Mem_U$|Precond||
|V.2|KernelMemorySafe|The function should not affect kernel's memory safety|Hazard||
|V.3|Section(val, section)|reside in binary section|Precond||
|VI.1|MutAccess(val)|has xclusive mutable access (to ports, registers) during runtime|Hazard||
|VI.2|UnAltered(val)|$\neg \Box(alter(val))$|Hazard||
|VI.3|Unaccessed(val)|$\neg \exist access(val)$|Precond||
|VI.4|Bounded(val, bound)|TBD|Precond||
|VI.5|LockHeld(val)|lock held|Precond||
|VI.6|ReferTo(func)|same SP as `func`|Precond||
|VI.7|Sync(condition)|TBD|Precond||
