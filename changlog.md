### 修改日志

- 计算apk  
  Returns a_pk = blake2s(1100 || [a_sk]_250 || 0^254)
 替换为
Returns a_pk = poseidon(0010 || [a_sk]_250 || 0)
 
 - **计算nullifier**   
Returns nf = blake2s(1110 || [a_sk]_252 || rho)  
替换为  
Returns nf = poseidon(1010 || [a_sk]_250 || rho).  
- 计算commit：  
inner_k = blake2s(r || a_pk || rho || V)  
替换为  
inner_k = poseidon(r || a_pk[:94] || rho[:94] || v)

- 计算rho:  
Returns rho_i = blake2s(0 || i || 10 || [phi]_252 || hsig）  
替换为  
Returns rho_i = poseidon(0 || i || 10 || [phi]_250 || hsig)     


- 计算merkel树根  
Mimc(left,right)  
替换为  
Poseidon(left,right)  
