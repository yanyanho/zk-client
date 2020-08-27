yum install python-devel mysql-devel
## 用户手册
 此服务提供BAC的匿名转账功能；  
 1 导入/或生成fisco地址  
 2 生成ZKBAC地址（匿名转账所需的地址）  
 3 存入资产，获取utxo  
 4 转账  
 5 取出资产  
 
 ## 转账原理
  转账为两入两出模型；
  inputs1 ---|------output1                     
  inputs2 ---|------output2
   (zethaddress:value) utxo模型
   
  ``` 
    def joinsplit(
            self,
            mk_tree: MerkleTree,
            sender_ownership_keypair: OwnershipKeyPair,
            sender_eth_address: str,
            inputs: List[Tuple[int, ZethNote]],
            outputs: List[Tuple[ZethAddressPub, EtherValue]],
            v_in: EtherValue,
            v_out: EtherValue,
            tx_value: Optional[EtherValue] = None,
            compute_h_sig_cb: Optional[ComputeHSigCB] = None) -> str:      
   ```  
```
function mix(
        uint256[2] memory a,
        uint256[4] memory b,
        uint256[2] memory c,
        uint256[4] memory vk,
        uint256 sigma,
        uint256[nbInputs] memory input,
        bytes[jsOut] memory ciphertexts)     
```

solidity input
```
 // ====================================================================== //
    // Reminder: Remember that the primary inputs are ordered as follows:
    //
    //   [Root, CommitmentS, NullifierS, h_sig, h_iS, Residual Field Element(S)]
    //
    // ie, below is the index mapping of the primary input elements on the
    // protoboard:
    //
    // - Index of the "Root" field elements: {0}
    // - Index of the "CommitmentS" field elements: [1, 1 + NumOutputs[
    // - Index of the "NullifierS" field elements:
    //   [1 + NumOutputs, 1 + NumOutputs + NumInputs[
    // - Index of the "h_sig" field element: {1 + NumOutputs + NumInputs}
    // - Index of the "Message Authentication TagS" (h_i) field elements:
    //   [1 + NumOutputs + NumInputs + 1,
    //    1 + NumOutputs + NumInputs + 1 + NumInputs[
    // - Index of the "Residual Field Element(s)" field elements:
    //   [1 + NumOutputs + NumInputs + 1 + NumInputs,
    //    1 + NumOutputs + NumInputs + 1 + NumInputs + nb_field_residual[
    //

    // digest_length=256   field_capacity=253  public_value_length = 64
    // The Residual field elements are structured as follows:
    // - v_pub_in [0, public_value_length[    0-64
    // - v_pub_out [public_value_length, 2*public_value_length[   64-128
    // - h_sig remaining bits    
    //   [2*public_value_length,              128 - 131
    //    2*public_value_length + (digest_length-field_capacity)[
    // - nullifierS remaining bits:             131-137
    //   [2*public_value_length + (digest_length-field_capacity),
    //    2*public_value_length + (1+NumInputs)*(digest_length-field_capacity)[
    // - message authentication tagS remaining bits:   137 -143
    //   [2*public_value_length + (1+NumInputs)*(digest_length-field_capacity),
    //    2*public_value_length + (1+2*NumInputs)*(digest_length-field_capacity)]
    // ============================================================================================ //
```