# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+
'''
from commands.utils import \
    open_web3_from_ctx, get_erc20_instance_description, load_eth_address, \
    write_mixer_description, MixerDescription
from zeth.mixer_client import MixerClient
from zeth.utils import EtherValue
'''
import json
import ast
from click import Context, command, option, pass_context
from typing import Optional
import sys
sys.path.append('../')
from python_web3.eth_utils import to_checksum_address
from python_web3.client.bcosclient import BcosClient
from contract.Groth16Mixer import Groth16Mixer
from zeth.prover_client import ProverClient
from zeth.mixer_client import write_verification_key
from zeth.zksnark import get_zksnark_provider
from commands.constants import PROVER_SERVER_ENDPOINT_DEFAULT


def deploy(
        token_address: Optional[str]
        ) :
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    zksnark = get_zksnark_provider("GROTH16")
    prover_client = ProverClient(PROVER_SERVER_ENDPOINT_DEFAULT)
    vk_obj = prover_client.get_verification_key()
    vk_json = zksnark.parse_verification_key(vk_obj)
    #print("VK.json: ", vk_json)

    print("Received VK, writing verification key...")
    write_verification_key(vk_json)
    verification_key_params = zksnark.verification_key_parameters(vk_json)
    constructArgs = [5, to_checksum_address(token_address), verification_key_params['Alpha'], verification_key_params['Beta1'], verification_key_params['Beta2'], verification_key_params['Delta1'], verification_key_params['Delta2'], verification_key_params['ABC_coords']]

    si = Groth16Mixer("")
    '''
    fo = open("./contract/mixer/abi/Groth16Mixer.abi")
    abistring = fo.read()
    abi = json.loads(abistring)
    fo.close()
    f1 = open("./contract/mixer/abi/Groth16Mixer.bin")
    bin = f1.read()
    f1.close()
    '''

    abi = [{'inputs': [{'internalType': 'uint256', 'name': 'mk_depth', 'type': 'uint256'}, {'internalType': 'address', 'name': 'token', 'type': 'address'}, {'internalType': 'uint256[2]', 'name': 'Alpha', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[]', 'name': 'ABC_coords', 'type': 'uint256[]'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'message', 'type': 'string'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'bytes32', 'name': 'message', 'type': 'bytes32'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint256', 'name': 'mid', 'type': 'uint256'}, {'indexed': False, 'internalType': 'bytes32', 'name': 'root', 'type': 'bytes32'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'nullifiers', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'commitments', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'LogMix', 'type': 'event'}, {'constant': True, 'inputs': [{'internalType': 'uint256[10]', 'name': 'primary_inputs', 'type': 'uint256[10]'}], 'name': 'assemble_hsig', 'outputs': [{'internalType': 'bytes32', 'name': 'hsig', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': 'index', 'type': 'uint256'}, {'internalType': 'uint256[10]', 'name': 'primary_inputs', 'type': 'uint256[10]'}], 'name': 'assemble_nullifier', 'outputs': [{'internalType': 'bytes32', 'name': 'nf', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256[10]', 'name': 'primary_inputs', 'type': 'uint256[10]'}], 'name': 'assemble_public_values', 'outputs': [{'internalType': 'uint256', 'name': 'vpub_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'vpub_out', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'get_constants', 'outputs': [{'internalType': 'uint256', 'name': 'js_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'js_out', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'num_inputs', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'bytes32', 'name': 'commitment', 'type': 'bytes32'}], 'name': 'insert', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'mid', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256[2]', 'name': 'a', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'b', 'type': 'uint256[4]'}, {'internalType': 'uint256[2]', 'name': 'c', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'vk', 'type': 'uint256[4]'}, {'internalType': 'uint256', 'name': 'sigma', 'type': 'uint256'}, {'internalType': 'uint256[10]', 'name': 'input', 'type': 'uint256[10]'}, {'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'mix', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}, {'internalType': 'bytes', 'name': '', 'type': 'bytes'}], 'name': 'onBAC001Received', 'outputs': [{'internalType': 'bytes4', 'name': '', 'type': 'bytes4'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'token', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}]

    binstr = "6080604052600080553480156200001557600080fd5b506040516200393b3803806200393b83398181016040526200003b9190810190620006cf565b878781806005811462000085576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016200007c9062000904565b60405180910390fd5b50620000966200042960201b60201c565b506000600160008081526020019081526020016000206000603f8110620000b957fe5b01549050600160036000808152602001908152602001600020600083815260200190815260200160002060006101000a81548160ff02191690831515021790555081600560006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061010060fd1062000183576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016200017a90620008c0565b60405180910390fd5b60fd6002800260010160fd610100030260406002020110620001dc576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401620001d390620008e2565b60405180910390fd5b505050604051806040016040528087600060028110620001f857fe5b60200201518152602001876001600281106200021057fe5b6020020151815250600660000160008201518160000155602082015181600101559050506040518060800160405280866000600281106200024d57fe5b60200201518152602001866001600281106200026557fe5b60200201518152602001856000600281106200027d57fe5b60200201518152602001856001600281106200029557fe5b6020020151815250600660020160008201518160000155602082015181600101556040820151816002015560608201518160030155905050604051806080016040528084600060028110620002e657fe5b6020020151815260200184600160028110620002fe57fe5b60200201518152602001836000600281106200031657fe5b60200201518152602001836001600281106200032e57fe5b6020020151815250600680016000820151816000015560208201518160010155604082015181600201556060820151816003015590505060008090505b60028251816200037757fe5b046006600a0180549050146200041a576006600a016040518060400160405280848481518110620003a457fe5b60200260200101518152602001846001850181518110620003c157fe5b60200260200101518152509080600181540180825580915050906001820390600052602060002090600202016000909192909190915060008201518160000155602082015181600101555050506002810190506200036b565b50505050505050505062000a23565b60008060001b90508060016000805481526020019081526020016000206002600560020a60020203603f81106200045c57fe5b018190555060006002600560020a816200047257fe5b0490505b6000811115620004df57620004978283620004e360201b620011e91760201c565b9150600060028260020203905082600160008054815260200190815260200160002082603f8110620004c557fe5b018190555060028281620004d557fe5b0491505062000476565b5050565b60007fdec937b7fa8db3de380427a8cc947bfab68514522c3439cfa2e99655098368146000527f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000018284828282088381820984858383098683840909925060005b605a8112156200057e57602060002080600052868688838808089350868485099250868488858a878809090994505060018101905062000543565b508484868a8888880808089550505050505092915050565b600081519050620005a781620009ef565b92915050565b600082601f830112620005bf57600080fd5b6002620005d6620005d08262000954565b62000926565b91508183856020840282011115620005ed57600080fd5b60005b83811015620006215781620006068882620006b8565b845260208401935060208301925050600181019050620005f0565b5050505092915050565b600082601f8301126200063d57600080fd5b8151620006546200064e8262000977565b62000926565b915081818352602084019350602081019050838560208402820111156200067a57600080fd5b60005b83811015620006ae5781620006938882620006b8565b8452602084019350602083019250506001810190506200067d565b5050505092915050565b600081519050620006c98162000a09565b92915050565b6000806000806000806000806101a0898b031215620006ed57600080fd5b6000620006fd8b828c01620006b8565b9850506020620007108b828c0162000596565b9750506040620007238b828c01620005ad565b9650506080620007368b828c01620005ad565b95505060c0620007498b828c01620005ad565b9450506101006200075d8b828c01620005ad565b935050610140620007718b828c01620005ad565b92505061018089015167ffffffffffffffff8111156200079057600080fd5b6200079e8b828c016200062b565b9150509295985092959890939650565b6000620007bd602d83620009a0565b91507f41206861736820646967657374206669747320696e20612073696e676c65206660008301527f69656c6420656c656d656e742e000000000000000000000000000000000000006020830152604082019050919050565b600062000825602b83620009a0565b91507f546f6f206d616e7920696e70757420616e64206f7574707574206e6f7465732060008301527f636f6e736964657265642e0000000000000000000000000000000000000000006020830152604082019050919050565b60006200088d601f83620009a0565b91507f496e76616c696420646570746820696e20426173654d65726b6c6554726565006000830152602082019050919050565b60006020820190508181036000830152620008db81620007ae565b9050919050565b60006020820190508181036000830152620008fd8162000816565b9050919050565b600060208201905081810360008301526200091f816200087e565b9050919050565b6000604051905081810181811067ffffffffffffffff821117156200094a57600080fd5b8060405250919050565b600067ffffffffffffffff8211156200096c57600080fd5b602082029050919050565b600067ffffffffffffffff8211156200098f57600080fd5b602082029050602081019050919050565b600082825260208201905092915050565b6000620009be82620009c5565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b620009fa81620009b1565b811462000a0657600080fd5b50565b62000a1481620009e5565b811462000a2057600080fd5b50565b612f088062000a336000396000f3fe6080604052600436106100865760003560e01c80634773862d116100595780634773862d1461015a578063a52f1ea814610176578063c73d16ae146101b3578063f9eb943f146101f0578063fc0c546a1461021d57610086565b80632d287e431461008b5780632e94420f146100b45780633e49ba65146100df57806346deb3411461011d575b600080fd5b34801561009757600080fd5b506100b260048036036100ad9190810190611cd7565b610248565b005b3480156100c057600080fd5b506100c9610318565b6040516100d69190612a59565b60405180910390f35b3480156100eb57600080fd5b5061010660048036036101019190810190611bf2565b61031e565b604051610114929190612ace565b60405180910390f35b34801561012957600080fd5b50610144600480360361013f9190810190611bf2565b61039a565b6040516101519190612843565b60405180910390f35b610174600480360361016f9190810190611c1c565b610417565b005b34801561018257600080fd5b5061019d60048036036101989190810190611d29565b61063d565b6040516101aa9190612843565b60405180910390f35b3480156101bf57600080fd5b506101da60048036036101d59190810190611b77565b61075b565b6040516101e7919061285e565b60405180910390f35b3480156101fc57600080fd5b5061020561076f565b60405161021493929190612af7565b60405180910390f35b34801561022957600080fd5b50610232610792565b60405161023f91906127a2565b60405180910390f35b600560020a600254141561028157600160005401600081905550600560020a6002548161027157fe5b066002819055506102806107b8565b5b600560020a600254106102c9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102c0906128f9565b60405180910390fd5b60006002549050600260008154600101919050819055506000816001600560020a0301905082600160008054815260200190815260200160002082603f811061030e57fe5b0181905550505050565b60005481565b600080600083600280026001016002800101600a811061033a57fe5b602002015190506002800260010160fd610100030281901c905064e8d4a5100067ffffffffffffffff168167ffffffffffffffff1602915064e8d4a5100067ffffffffffffffff16604082901c67ffffffffffffffff1602925050915091565b60008060fd60406002026002800260010160fd6101000302604060020201610100030184600280026001016002800101600a81106103d457fe5b602002015160001b901b901c9050600060fd610100038460028060020101600a81106103fc57fe5b6020020151901b90508160001c810160001b92505050919050565b61041f61180e565b61042a85848361085f565b600060023373ffffffffffffffffffffffffffffffffffffffff168460006002811061045257fe5b60200201518560016002811061046457fe5b60200201518c8c8c8a6040516020016104839796959493929190612728565b60405160208183030381529060405260405161049f91906126fc565b602060405180830381855afa1580156104bc573d6000803e3d6000fd5b5050506040513d601f19601f820116820180604052506104df9190810190611d00565b9050610533866000600481106104f157fe5b60200201518760016004811061050357fe5b60200201518860026004811061051557fe5b60200201518960036004811061052757fe5b60200201518986610a41565b610572576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610569906129f9565b60405180910390fd5b61057e89898987610b18565b6105bd576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105b490612999565b60405180910390fd5b6105c561180e565b6105cf8582610d1f565b60006105db6002610d7b565b90506105e681610df0565b7f5b20d7b970f991ad433adaa73d15ec55f2dc64ddfecb9505eb1f94e330ecddf76000548286858960405161061f959493929190612a74565b60405180910390a161063086610e31565b5050505050505050505050565b600060028310610682576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161067990612879565b60405180910390fd5b600060fd610100038460010102604060020201905060fd61010003810160fd10156106e2576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106d990612919565b60405180910390fd5b600060fd826002800260010160fd6101000302604060020201610100030185600280026001016002800101600a811061071757fe5b602002015160001b901b901c9050600060fd6101000385876002800101600a811061073e57fe5b6020020151901b90508160001c810160001b935050505092915050565b600063c73d16ae60e01b9050949350505050565b600080600060029250600291506001600280026001016002800101019050909192565b600560009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60008060001b90508060016000805481526020019081526020016000206002600560020a60020203603f81106107ea57fe5b018190555060006002600560020a816107ff57fe5b0490505b600081111561085b5761081682836111e9565b9150600060028260020203905082600160008054815260200190815260200160002082603f811061084357fe5b01819055506002828161085257fe5b04915050610803565b5050565b6108688261129a565b6108a7576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161089e90612939565b60405180910390fd5b60008090505b60028110156109755760006108c2828561063d565b90506004600082815260200190815260200160002060009054906101000a900460ff1615610925576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161091c90612899565b60405180910390fd5b60016004600083815260200190815260200160002060006101000a81548160ff0219169083151502179055508083836002811061095e57fe5b6020020181815250505080806001019150506108ad565b5060006002828560405160200161098d9291906126d0565b6040516020818303038152906040526040516109a991906126fc565b602060405180830381855afa1580156109c6573d6000803e3d6000fd5b5050506040513d601f19601f820116820180604052506109e99190810190611d00565b905060006109f68461039a565b9050808214610a3a576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610a3190612959565b60405180910390fd5b5050505050565b6000610a4b611830565b6107d05a038682528560208301528360408301526020608083016060846000600286f150604082018981528860208201526040816060836000600787f1506040836080856000600687f15060016040840152600260608401528560808401526040816060836000600787f150505080600260058110610ac657fe5b602002015181600060058110610ad857fe5b6020020151148015610b0b575080600360058110610af257fe5b602002015181600160058110610b0457fe5b6020020151145b9150509695505050505050565b6000807f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000019050610b46611852565b86600060028110610b5357fe5b602002015181600001818152505086600160028110610b6e57fe5b602002015181602001818152505085600060048110610b8957fe5b602002015181604001818152505085600160048110610ba457fe5b602002015181606001818152505085600260048110610bbf57fe5b602002015181608001818152505085600360048110610bda57fe5b60200201518160a001818152505084600060028110610bf557fe5b60200201518160c001818152505084600160028110610c1057fe5b60200201518160e00181815250506060600160028002600101600280010101604051908082528060200260200182016040528015610c5d5781602001602082028038833980820191505090505b50905060008090505b600160028002600101600280010101811015610d0457838682600a8110610c8957fe5b602002015110610cce576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610cc5906129d9565b60405180910390fd5b8581600a8110610cda57fe5b6020020151828281518110610ceb57fe5b6020026020010181815250508080600101915050610c66565b50610d0f8183611385565b6001149350505050949350505050565b60008090505b6002811015610d765760008382600201600a8110610d3f57fe5b602002015160001b905080838360028110610d5657fe5b602002018181525050610d6881610248565b508080600101915050610d25565b505050565b60008060025490506000836002540390506000600560020a90505b6001811115610dc457610daa8183856116a1565b809450819350505060028181610dbc57fe5b049050610d96565b60016000805481526020019081526020016000206000603f8110610de457fe5b01549350505050919050565b60016003600080548152602001908152602001600020600083815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b600080610e3d8361031e565b915091506000821115610f8457600073ffffffffffffffffffffffffffffffffffffffff16600560009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614610f3c576000600560009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff1663d0e7d6113330866040518463ffffffff1660e01b8152600401610f04939291906127bd565b600060405180830381600087803b158015610f1e57600080fd5b505af1158015610f32573d6000803e3d6000fd5b5050505050610f7f565b813414610f7e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610f75906129b9565b60405180910390fd5b5b61103c565b600034111561103b5760003373ffffffffffffffffffffffffffffffffffffffff1634604051610fb390612713565b60006040518083038185875af1925050503d8060008114610ff0576040519150601f19603f3d011682016040523d82523d6000602084013e610ff5565b606091505b5050905080611039576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611030906128b9565b60405180910390fd5b505b5b60008111156111e457600073ffffffffffffffffffffffffffffffffffffffff16600560009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614611135576000600560009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff16639bd9bbc633846040518363ffffffff1660e01b81526004016110fd929190612807565b600060405180830381600087803b15801561111757600080fd5b505af115801561112b573d6000803e3d6000fd5b50505050506111e3565b60003373ffffffffffffffffffffffffffffffffffffffff168260405161115b90612713565b60006040518083038185875af1925050503d8060008114611198576040519150601f19603f3d011682016040523d82523d6000602084013e61119d565b606091505b50509050806111e1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016111d8906128d9565b60405180910390fd5b505b5b505050565b60007fdec937b7fa8db3de380427a8cc947bfab68514522c3439cfa2e99655098368146000527f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000018284828282088381820984858383098683840909925060005b605a81121561128257602060002080600052868688838808089350868485099250868488858a8788090909945050600181019050611249565b508484868a8888880808089550505050505092915050565b6000806000905060008090505b600054811161137957600360008281526020019081526020016000206000856000600a81106112d257fe5b602002015160001b815260200190815260200160002060009054906101000a900460ff16156113045781806001019250505b600360008281526020019081526020016000206000856001600a811061132657fe5b602002015160001b815260200190815260200160002060009054906101000a900460ff16156113585781806001019250505b600282141561136c57600192505050611380565b80806001019150506112a7565b5060009150505b919050565b60006006600a01805490506001845101146113d5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016113cc90612979565b60405180910390fd5b6113dd611897565b6000600190506107d05a03600a60060183526020832060208701875160200281018254865260018301546020870152600283019250604086015b8183101561146657835481526001840154602082015282516040820152604081606083600060078af160408860808a600060068bf1808216881697505050600284019350602083019250611417565b5050505050806114ab576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016114a290612a39565b60405180910390fd5b7f198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c260408301527f1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed60608301527f090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b60808301527f12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa60a083015260065460c083015260016006015460e083015260026006015461010083015260036006015461012083015260046006015461014083015260056006015461016083015283516101808301527f30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47602085015181810682036101a085015260408601516101c085015260608601516101e0850152608086015161020085015260a086015161022085015260c086015161024085015260e086015161026085015260068001546102808501526007600601546102a08501526008600601546102c08501526009600601546102e085015260208461030086600060086107d05a03f19250505080611685576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161167c90612a19565b60405180910390fd5b8160006018811061169257fe5b60200201519250505092915050565b60008060006001860390506000600119861682019050600080600187161461174e576001868401039050611718600160008054815260200190815260200160002082603f81106116ed57fe5b0154600160008054815260200190815260200160002085600202603f811061171157fe5b01546111e9565b60016000805481526020019081526020016000206002600184038161173957fe5b04603f811061174457fe5b0181905550611754565b85830190505b5b818111156117e6576002810390506117b0600160008054815260200190815260200160002082603f811061178557fe5b0154600160008054815260200190815260200160002060018401603f81106117a957fe5b01546111e9565b6001600080548152602001908152602001600020600260018403816117d157fe5b04603f81106117dc57fe5b0181905550611755565b600287816117f057fe5b04600260018801816117fe57fe5b0494509450505050935093915050565b6040518060400160405280600290602082028038833980820191505090505090565b6040518060a00160405280600590602082028038833980820191505090505090565b60405180610100016040528060008152602001600081526020016000815260200160008152602001600081526020016000815260200160008152602001600081525090565b604051806103000160405280601890602082028038833980820191505090505090565b6000813590506118c981612e80565b92915050565b600082601f8301126118e057600080fd5b60026118f36118ee82612b5b565b612b2e565b9150818360005b8381101561192a57813586016119108882611aba565b8452602084019350602083019250506001810190506118fa565b5050505092915050565b600082601f83011261194557600080fd5b600a61195861195382612b7d565b612b2e565b9150818385602084028201111561196e57600080fd5b60005b8381101561199e57816119848882611b62565b845260208401935060208301925050600181019050611971565b5050505092915050565b600082601f8301126119b957600080fd5b60026119cc6119c782612b9f565b612b2e565b915081838560208402820111156119e257600080fd5b60005b83811015611a1257816119f88882611b62565b8452602084019350602083019250506001810190506119e5565b5050505092915050565b600082601f830112611a2d57600080fd5b6004611a40611a3b82612bc1565b612b2e565b91508183856020840282011115611a5657600080fd5b60005b83811015611a865781611a6c8882611b62565b845260208401935060208301925050600181019050611a59565b5050505092915050565b600081359050611a9f81612e97565b92915050565b600081519050611ab481612e97565b92915050565b600082601f830112611acb57600080fd5b8135611ade611ad982612be3565b612b2e565b91508082526020830160208301858383011115611afa57600080fd5b611b05838284612e23565b50505092915050565b600082601f830112611b1f57600080fd5b8135611b32611b2d82612c0f565b612b2e565b91508082526020830160208301858383011115611b4e57600080fd5b611b59838284612e23565b50505092915050565b600081359050611b7181612eae565b92915050565b60008060008060808587031215611b8d57600080fd5b6000611b9b878288016118ba565b9450506020611bac878288016118ba565b9350506040611bbd87828801611b62565b925050606085013567ffffffffffffffff811115611bda57600080fd5b611be687828801611b0e565b91505092959194509250565b60006101408284031215611c0557600080fd5b6000611c1384828501611934565b91505092915050565b6000806000806000806000610300888a031215611c3857600080fd5b6000611c468a828b016119a8565b9750506040611c578a828b01611a1c565b96505060c0611c688a828b016119a8565b955050610100611c7a8a828b01611a1c565b945050610180611c8c8a828b01611b62565b9350506101a0611c9e8a828b01611934565b9250506102e088013567ffffffffffffffff811115611cbc57600080fd5b611cc88a828b016118cf565b91505092959891949750929550565b600060208284031215611ce957600080fd5b6000611cf784828501611a90565b91505092915050565b600060208284031215611d1257600080fd5b6000611d2084828501611aa5565b91505092915050565b6000806101608385031215611d3d57600080fd5b6000611d4b85828601611b62565b9250506020611d5c85828601611934565b9150509250929050565b6000611d728383612008565b60208301905092915050565b6000611d8a8383612026565b60208301905092915050565b6000611da28383612075565b905092915050565b6000611db683836126aa565b60208301905092915050565b611dcb81612ded565b82525050565b611dda81612d7b565b82525050565b611de981612c6d565b611df38184612cfb565b9250611dfe82612c3b565b8060005b83811015611e2f578151611e168782611d66565b9650611e2183612cba565b925050600181019050611e02565b505050505050565b611e4081612c6d565b611e4a8184612d06565b9250611e5582612c3b565b8060005b83811015611e86578151611e6d8782611d7e565b9650611e7883612cba565b925050600181019050611e59565b505050505050565b6000611e9982612c78565b611ea38185612d11565b935083602082028501611eb585612c45565b8060005b85811015611ef15784840389528151611ed28582611d96565b9450611edd83612cc7565b925060208a01995050600181019050611eb9565b50829750879550505050505092915050565b611f0c81612c83565b611f168184612d1c565b9250611f2182612c4f565b8060005b83811015611f52578151611f398782611daa565b9650611f4483612cd4565b925050600181019050611f25565b505050505050565b611f6381612c8e565b611f6d8184612d27565b9250611f7882612c59565b8060005b83811015611fa9578151611f908782611daa565b9650611f9b83612ce1565b925050600181019050611f7c565b505050505050565b611fba81612c99565b611fc48184612d32565b9250611fcf82612c63565b8060005b83811015612000578151611fe78782611daa565b9650611ff283612cee565b925050600181019050611fd3565b505050505050565b61201181612d8d565b82525050565b61202081612d8d565b82525050565b61202f81612d8d565b82525050565b61203e81612d97565b82525050565b600061204f82612caf565b6120598185612d5f565b9350612069818560208601612e32565b80840191505092915050565b600061208082612ca4565b61208a8185612d3d565b935061209a818560208601612e32565b6120a381612e6f565b840191505092915050565b60006120b982612ca4565b6120c38185612d5f565b93506120d3818560208601612e32565b80840191505092915050565b60006120ec601883612d6a565b91507f6e756c6c696669657220696e646578206f766572666c6f7700000000000000006000830152602082019050919050565b600061212c603783612d6a565b91507f496e76616c6964206e756c6c69666965723a2054686973206e756c6c6966696560008301527f722068617320616c7265616479206265656e20757365640000000000000000006020830152604082019050919050565b6000612192601e83612d6a565b91507f767075625f696e2072657475726e207472616e73666572206661696c656400006000830152602082019050919050565b60006121d2601883612d6a565b91507f767075625f6f7574207472616e73666572206661696c656400000000000000006000830152602082019050919050565b6000612212602783612d6a565b91507f4d65726b6c6520747265652066756c6c3a2043616e6e6f7420617070656e642060008301527f616e796d6f7265000000000000000000000000000000000000000000000000006020830152604082019050919050565b6000612278603083612d6a565b91507f6e756c6c6966696572207772697474656e20696e20646966666572656e74207260008301527f6573696475616c2062697420662e652e000000000000000000000000000000006020830152604082019050919050565b60006122de602583612d6a565b91507f496e76616c696420726f6f743a205468697320726f6f7420646f65736e27742060008301527f65786973740000000000000000000000000000000000000000000000000000006020830152604082019050919050565b6000612344604983612d6a565b91507f496e76616c696420687369673a2054686973206873696720646f6573206e6f7460008301527f20636f72726573706f6e6420746f207468652068617368206f6620766b20616e60208301527f6420746865206e667300000000000000000000000000000000000000000000006040830152606082019050919050565b60006123d0602283612d6a565b91507f496e707574206c656e67746820646966666572732066726f6d2065787065637460008301527f65640000000000000000000000000000000000000000000000000000000000006020830152604082019050919050565b6000612436603383612d6a565b91507f496e76616c69642070726f6f663a20556e61626c6520746f207665726966792060008301527f7468652070726f6f6620636f72726563746c79000000000000000000000000006020830152604082019050919050565b600061249c602a83612d6a565b91507f57726f6e67206d73672e76616c75653a2056616c75652070616964206973206e60008301527f6f7420636f7272656374000000000000000000000000000000000000000000006020830152604082019050919050565b6000612502601c83612d6a565b91507f496e707574206973206e6f7420696e207363616c6172206669656c64000000006000830152602082019050919050565b6000612542603b83612d6a565b91507f496e76616c6964207369676e61747572653a20556e61626c6520746f2076657260008301527f69667920746865207369676e617475726520636f72726563746c7900000000006020830152604082019050919050565b60006125a8600083612d4e565b9150600082019050919050565b60006125c2600083612d5f565b9150600082019050919050565b60006125dc603783612d6a565b91507f43616c6c20746f20626e3235364164642c20626e3235365363616c61724d756c60008301527f206f7220626e32353650616972696e67206661696c65640000000000000000006020830152604082019050919050565b6000612642603983612d6a565b91507f43616c6c20746f2074686520626e323536416464206f7220626e32353653636160008301527f6c61724d756c20707265636f6d70696c6564206661696c6564000000000000006020830152604082019050919050565b6126a481612de3565b82525050565b6126b381612de3565b82525050565b6126ca6126c582612de3565b612e65565b82525050565b60006126dc8285611e37565b6040820191506126ec8284611fb1565b6080820191508190509392505050565b60006127088284612044565b915081905092915050565b600061271e826125b5565b9150819050919050565b6000612734828a6126b9565b60208201915061274482896120ae565b915061275082886120ae565b915061275c8287611f5a565b60408201915061276c8286611fb1565b60808201915061277c8285611f5a565b60408201915061278c8284611f03565b6101408201915081905098975050505050505050565b60006020820190506127b76000830184611dd1565b92915050565b60006080820190506127d26000830186611dc2565b6127df6020830185611dd1565b6127ec604083018461269b565b81810360608301526127fd8161259b565b9050949350505050565b600060608201905061281c6000830185611dc2565b612829602083018461269b565b818103604083015261283a8161259b565b90509392505050565b60006020820190506128586000830184612017565b92915050565b60006020820190506128736000830184612035565b92915050565b60006020820190508181036000830152612892816120df565b9050919050565b600060208201905081810360008301526128b28161211f565b9050919050565b600060208201905081810360008301526128d281612185565b9050919050565b600060208201905081810360008301526128f2816121c5565b9050919050565b6000602082019050818103600083015261291281612205565b9050919050565b600060208201905081810360008301526129328161226b565b9050919050565b60006020820190508181036000830152612952816122d1565b9050919050565b6000602082019050818103600083015261297281612337565b9050919050565b60006020820190508181036000830152612992816123c3565b9050919050565b600060208201905081810360008301526129b281612429565b9050919050565b600060208201905081810360008301526129d28161248f565b9050919050565b600060208201905081810360008301526129f2816124f5565b9050919050565b60006020820190508181036000830152612a1281612535565b9050919050565b60006020820190508181036000830152612a32816125cf565b9050919050565b60006020820190508181036000830152612a5281612635565b9050919050565b6000602082019050612a6e600083018461269b565b92915050565b600060e082019050612a89600083018861269b565b612a966020830187612017565b612aa36040830186611de0565b612ab06080830185611de0565b81810360c0830152612ac28184611e8e565b90509695505050505050565b6000604082019050612ae3600083018561269b565b612af0602083018461269b565b9392505050565b6000606082019050612b0c600083018661269b565b612b19602083018561269b565b612b26604083018461269b565b949350505050565b6000604051905081810181811067ffffffffffffffff82111715612b5157600080fd5b8060405250919050565b600067ffffffffffffffff821115612b7257600080fd5b602082029050919050565b600067ffffffffffffffff821115612b9457600080fd5b602082029050919050565b600067ffffffffffffffff821115612bb657600080fd5b602082029050919050565b600067ffffffffffffffff821115612bd857600080fd5b602082029050919050565b600067ffffffffffffffff821115612bfa57600080fd5b601f19601f8301169050602081019050919050565b600067ffffffffffffffff821115612c2657600080fd5b601f19601f8301169050602081019050919050565b6000819050919050565b6000819050919050565b6000819050919050565b6000819050919050565b6000819050919050565b600060029050919050565b600060029050919050565b6000600a9050919050565b600060029050919050565b600060049050919050565b600081519050919050565b600081519050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600082825260208201905092915050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b6000612d8682612dc3565b9050919050565b6000819050919050565b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b6000612df882612dff565b9050919050565b6000612e0a82612e11565b9050919050565b6000612e1c82612dc3565b9050919050565b82818337600083830152505050565b60005b83811015612e50578082015181840152602081019050612e35565b83811115612e5f576000848401525b50505050565b6000819050919050565b6000601f19601f8301169050919050565b612e8981612d7b565b8114612e9457600080fd5b50565b612ea081612d8d565b8114612eab57600080fd5b50565b612eb781612de3565b8114612ec257600080fd5b5056fea365627a7a72315820f62d867b7f806cc547daab622cb427ec98c2222a4a755612cb1dc066faf41a526c6578706572696d656e74616cf564736f6c63430005110040"

    # with open("./contract/mixer/abi/Groth16Mixer.abi", "r") as abistring:
    #     abistr = abistring.readlines()[0]
    #     abi = ast.literal_eval(abistr)
    # with open("./contract/mixer/abi/Groth16Mixer.bin", "r") as binstring:
    #     binstr = binstring.readlines()[0]

    client = BcosClient()
    mixerTransactionRecipient = client.sendRawTransactionGetReceipt("", abi, None, constructArgs, binstr)
    mixer_address = mixerTransactionRecipient['contractAddress']
    print(f"deploy: mixer_address={mixer_address}")
    #mixer_instance = Groth16Mixer(address)
    return mixer_address


if __name__ == '__main__':
    deploy()

