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
        ) -> None:
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
    abi5 = [{'inputs': [{'internalType': 'uint256', 'name': 'mk_depth', 'type': 'uint256'}, {'internalType': 'address', 'name': 'token', 'type': 'address'}, {'internalType': 'uint256[2]', 'name': 'Alpha', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[]', 'name': 'ABC_coords', 'type': 'uint256[]'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'message', 'type': 'string'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'bytes32', 'name': 'message', 'type': 'bytes32'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'bytes32', 'name': 'root', 'type': 'bytes32'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'nullifiers', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'commitments', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'LogMix', 'type': 'event'}, {'constant': True, 'inputs': [{'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_hsig', 'outputs': [{'internalType': 'bytes32', 'name': 'hsig', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': 'index', 'type': 'uint256'}, {'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_nullifier', 'outputs': [{'internalType': 'bytes32', 'name': 'nf', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_public_values', 'outputs': [{'internalType': 'uint256', 'name': 'vpub_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'vpub_out', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'get_constants', 'outputs': [{'internalType': 'uint256', 'name': 'js_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'js_out', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'num_inputs', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'bytes32', 'name': 'commitment', 'type': 'bytes32'}], 'name': 'insert', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256[2]', 'name': 'a', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'b', 'type': 'uint256[4]'}, {'internalType': 'uint256[2]', 'name': 'c', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'vk', 'type': 'uint256[4]'}, {'internalType': 'uint256', 'name': 'sigma', 'type': 'uint256'}, {'internalType': 'uint256[9]', 'name': 'input', 'type': 'uint256[9]'}, {'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'mix', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'token', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'tokenFallback', 'outputs': [], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}]
    bin5 = "60806040523480156200001157600080fd5b50604051620037d3380380620037d3833981810160405262000037919081019062000685565b878781806005811462000081576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016200007890620008ba565b60405180910390fd5b50620000926200040360201b60201c565b506000806000603f8110620000a357fe5b0154905060016040600083815260200190815260200160002060006101000a81548160ff02191690831515021790555081604260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061010060fd106200015c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401620001539062000876565b60405180910390fd5b60fd6002800260010160fd610100030260406002020110620001b5576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401620001ac9062000898565b60405180910390fd5b505050604051806040016040528087600060028110620001d157fe5b6020020151815260200187600160028110620001e957fe5b6020020151815250604360000160008201518160000155602082015181600101559050506040518060800160405280866000600281106200022657fe5b60200201518152602001866001600281106200023e57fe5b60200201518152602001856000600281106200025657fe5b60200201518152602001856001600281106200026e57fe5b6020020151815250604360020160008201518160000155602082015181600101556040820151816002015560608201518160030155905050604051806080016040528084600060028110620002bf57fe5b6020020151815260200184600160028110620002d757fe5b6020020151815260200183600060028110620002ef57fe5b60200201518152602001836001600281106200030757fe5b602002015181525060436006016000820151816000015560208201518160010155604082015181600201556060820151816003015590505060008090505b60028251816200035157fe5b046043600a018054905014620003f4576043600a0160405180604001604052808484815181106200037e57fe5b602002602001015181526020018460018501815181106200039b57fe5b602002602001015181525090806001815401808255809150509060018203906000526020600020906002020160009091929091909150600082015181600001556020820151816001015550505060028101905062000345565b505050505050505050620009d9565b60008060001b90508060006002600560020a60020203603f81106200042457fe5b018190555060006002600560020a816200043a57fe5b0490505b600081111562000495576200045f82836200049960201b620016c61760201c565b9150600060028260020203905082600082603f81106200047b57fe5b0181905550600282816200048b57fe5b049150506200043e565b5050565b60007fdec937b7fa8db3de380427a8cc947bfab68514522c3439cfa2e99655098368146000527f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000018284828282088381820984858383098683840909925060005b605a8112156200053457602060002080600052868688838808089350868485099250868488858a8788090909945050600181019050620004f9565b508484868a8888880808089550505050505092915050565b6000815190506200055d81620009a5565b92915050565b600082601f8301126200057557600080fd5b60026200058c62000586826200090a565b620008dc565b91508183856020840282011115620005a357600080fd5b60005b83811015620005d75781620005bc88826200066e565b845260208401935060208301925050600181019050620005a6565b5050505092915050565b600082601f830112620005f357600080fd5b81516200060a62000604826200092d565b620008dc565b915081818352602084019350602081019050838560208402820111156200063057600080fd5b60005b838110156200066457816200064988826200066e565b84526020840193506020830192505060018101905062000633565b5050505092915050565b6000815190506200067f81620009bf565b92915050565b6000806000806000806000806101a0898b031215620006a357600080fd5b6000620006b38b828c016200066e565b9850506020620006c68b828c016200054c565b9750506040620006d98b828c0162000563565b9650506080620006ec8b828c0162000563565b95505060c0620006ff8b828c0162000563565b945050610100620007138b828c0162000563565b935050610140620007278b828c0162000563565b92505061018089015167ffffffffffffffff8111156200074657600080fd5b620007548b828c01620005e1565b9150509295985092959890939650565b600062000773602d8362000956565b91507f41206861736820646967657374206669747320696e20612073696e676c65206660008301527f69656c6420656c656d656e742e000000000000000000000000000000000000006020830152604082019050919050565b6000620007db602b8362000956565b91507f546f6f206d616e7920696e70757420616e64206f7574707574206e6f7465732060008301527f636f6e736964657265642e0000000000000000000000000000000000000000006020830152604082019050919050565b600062000843601f8362000956565b91507f496e76616c696420646570746820696e20426173654d65726b6c6554726565006000830152602082019050919050565b60006020820190508181036000830152620008918162000764565b9050919050565b60006020820190508181036000830152620008b381620007cc565b9050919050565b60006020820190508181036000830152620008d58162000834565b9050919050565b6000604051905081810181811067ffffffffffffffff821117156200090057600080fd5b8060405250919050565b600067ffffffffffffffff8211156200092257600080fd5b602082029050919050565b600067ffffffffffffffff8211156200094557600080fd5b602082029050602081019050919050565b600082825260208201905092915050565b600062000974826200097b565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b620009b08162000967565b8114620009bc57600080fd5b50565b620009ca816200099b565b8114620009d657600080fd5b50565b612dea80620009e96000396000f3fe60806040526004361061007b5760003560e01c806397e004891161004e57806397e0048914610161578063c0ee0b8a1461017d578063f9eb943f146101a6578063fc0c546a146101d35761007b565b806305ceb93c146100805780631f40927c146100bd5780632d287e43146100fb578063354d06fd14610124575b600080fd5b34801561008c57600080fd5b506100a760048036036100a29190810190611cdb565b6101fe565b6040516100b491906127a6565b60405180910390f35b3480156100c957600080fd5b506100e460048036036100df9190810190611c5f565b61031e565b6040516100f29291906129ed565b60405180910390f35b34801561010757600080fd5b50610122600480360361011d9190810190611c89565b61039b565b005b34801561013057600080fd5b5061014b60048036036101469190810190611c5f565b610420565b60405161015891906127a6565b60405180910390f35b61017b60048036036101769190810190611ba4565b61049e565b005b34801561018957600080fd5b506101a4600480360361019f9190810190611b3d565b6106c0565b005b3480156101b257600080fd5b506101bb6108cb565b6040516101ca93929190612a16565b60405180910390f35b3480156101df57600080fd5b506101e86108ef565b6040516101f5919061272b565b60405180910390f35b600060028310610243576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023a9061280d565b60405180910390fd5b600060fd610100038460010102604060020201905060fd61010003810160fd10156102a3576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161029a906128ad565b60405180910390fd5b600060fd826002800260010160fd610100030260406002020161010003018560028002600101600260010101600981106102d957fe5b602002015160001b901b901c9050600060fd6101000385876002600101016009811061030157fe5b6020020151901b90508160001c810160001b935050505092915050565b600080600083600280026001016002600101016009811061033b57fe5b602002015190506002800260010160fd610100030281901c905064e8d4a5100067ffffffffffffffff168167ffffffffffffffff1602915064e8d4a5100067ffffffffffffffff16604082901c67ffffffffffffffff1602925050915091565b600560020a603f54106103e3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103da9061288d565b60405180910390fd5b6000603f549050603f60008154600101919050819055506000816001600560020a0301905082600082603f811061041657fe5b0181905550505050565b60008060fd60406002026002800260010160fd6101000302604060020201610100030184600280026001016002600101016009811061045b57fe5b602002015160001b901b901c9050600060fd6101000384600280600101016009811061048357fe5b6020020151901b90508160001c810160001b92505050919050565b6104a6611777565b6104b1858483610915565b600060023373ffffffffffffffffffffffffffffffffffffffff16846000600281106104d957fe5b6020020151856001600281106104eb57fe5b60200201518c8c8c8a60405160200161050a97969594939291906126b1565b6040516020818303038152906040526040516105269190612685565b602060405180830381855afa158015610543573d6000803e3d6000fd5b5050506040513d601f19601f820116820180604052506105669190810190611cb2565b90506105ba8660006004811061057857fe5b60200201518760016004811061058a57fe5b60200201518860026004811061059c57fe5b6020020151896003600481106105ae57fe5b60200201518986610b23565b6105f9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105f09061298d565b60405180910390fd5b61060589898987610bfa565b610644576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161063b9061292d565b60405180910390fd5b61064c611777565b6106568582610e03565b60006106626002610e5f565b905061066d81610ec1565b7f36ed7c3f2ecfb5a5226c478b034d33144c060afe361be291e948f861dcddc618818584886040516106a294939291906127c1565b60405180910390a16106b386610ef0565b5050505050505050505050565b6106c8611799565b83816000019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff168152505082816020018181525050818160400181905250600060188360038151811061072457fe5b602001015160f81c60f81b7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff19167bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916901c60e01c60108460028151811061078457fe5b602001015160f81c60f81b7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff19167bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916901c60e01c6008856001815181106107e457fe5b602001015160f81c60f81b7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff19167bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916901c60e01c8560008151811061084257fe5b602001015160f81c60f81b7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff191660e01c01010190508060e01b82606001907bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191690817bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916815250505050505050565b60008060006002925060029150600160028002600101600260010101019050909192565b604260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b604060008360006009811061092657fe5b602002015160001b815260200190815260200160002060009054906101000a900460ff16610989576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610980906128cd565b60405180910390fd5b60008090505b6002811015610a575760006109a482856101fe565b90506041600082815260200190815260200160002060009054906101000a900460ff1615610a07576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109fe9061282d565b60405180910390fd5b60016041600083815260200190815260200160002060006101000a81548160ff02191690831515021790555080838360028110610a4057fe5b60200201818152505050808060010191505061098f565b50600060028285604051602001610a6f929190612659565b604051602081830303815290604052604051610a8b9190612685565b602060405180830381855afa158015610aa8573d6000803e3d6000fd5b5050506040513d601f19601f82011682018060405250610acb9190810190611cb2565b90506000610ad884610420565b9050808214610b1c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b13906128ed565b60405180910390fd5b5050505050565b6000610b2d6117f6565b6107d05a038682528560208301528360408301526020608083016060846000600286f150604082018981528860208201526040816060836000600787f1506040836080856000600687f15060016040840152600260608401528560808401526040816060836000600787f150505080600260058110610ba857fe5b602002015181600060058110610bba57fe5b6020020151148015610bed575080600360058110610bd457fe5b602002015181600160058110610be657fe5b6020020151145b9150509695505050505050565b6000807f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000019050610c28611818565b86600060028110610c3557fe5b602002015181600001818152505086600160028110610c5057fe5b602002015181602001818152505085600060048110610c6b57fe5b602002015181604001818152505085600160048110610c8657fe5b602002015181606001818152505085600260048110610ca157fe5b602002015181608001818152505085600360048110610cbc57fe5b60200201518160a001818152505084600060028110610cd757fe5b60200201518160c001818152505084600160028110610cf257fe5b60200201518160e0018181525050606060016002800260010160026001010101604051908082528060200260200182016040528015610d405781602001602082028038833980820191505090505b50905060008090505b60016002800260010160026001010101811015610de85783868260098110610d6d57fe5b602002015110610db2576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610da99061296d565b60405180910390fd5b858160098110610dbe57fe5b6020020151828281518110610dcf57fe5b6020026020010181815250508080600101915050610d49565b50610df381836112a8565b6001149350505050949350505050565b60008090505b6002811015610e5a576000838260010160098110610e2357fe5b602002015160001b905080838360028110610e3a57fe5b602002018181525050610e4c8161039b565b508080600101915050610e09565b505050565b600080603f549050600083603f540390506000600560020a90505b6001811115610ea857610e8e8183856115c5565b809450819350505060028181610ea057fe5b049050610e7a565b600080603f8110610eb557fe5b01549350505050919050565b60016040600083815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b600080610efc8361031e565b91509150600082111561104357600073ffffffffffffffffffffffffffffffffffffffff16604260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614610ffb576000604260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff166323b872dd3330866040518463ffffffff1660e01b8152600401610fc393929190612746565b600060405180830381600087803b158015610fdd57600080fd5b505af1158015610ff1573d6000803e3d6000fd5b505050505061103e565b81341461103d576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110349061294d565b60405180910390fd5b5b6110fb565b60003411156110fa5760003373ffffffffffffffffffffffffffffffffffffffff16346040516110729061269c565b60006040518083038185875af1925050503d80600081146110af576040519150601f19603f3d011682016040523d82523d6000602084013e6110b4565b606091505b50509050806110f8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110ef9061284d565b60405180910390fd5b505b5b60008111156112a357600073ffffffffffffffffffffffffffffffffffffffff16604260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16146111f4576000604260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690508073ffffffffffffffffffffffffffffffffffffffff1663a9059cbb33846040518363ffffffff1660e01b81526004016111bc92919061277d565b600060405180830381600087803b1580156111d657600080fd5b505af11580156111ea573d6000803e3d6000fd5b50505050506112a2565b60003373ffffffffffffffffffffffffffffffffffffffff168260405161121a9061269c565b60006040518083038185875af1925050503d8060008114611257576040519150601f19603f3d011682016040523d82523d6000602084013e61125c565b606091505b50509050806112a0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016112979061286d565b60405180910390fd5b505b5b505050565b60006043600a01805490506001845101146112f8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016112ef9061290d565b60405180910390fd5b61130061185d565b6000600190506107d05a03600a60430183526020832060208701875160200281018254865260018301546020870152600283019250604086015b8183101561138957835481526001840154602082015282516040820152604081606083600060078af160408860808a600060068bf180821688169750505060028401935060208301925061133a565b5050505050806113ce576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016113c5906129cd565b60405180910390fd5b7f198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c260408301527f1800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed60608301527f090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b60808301527f12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa60a083015260435460c083015260016043015460e083015260026043015461010083015260036043015461012083015260046043015461014083015260056043015461016083015283516101808301527f30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47602085015181810682036101a085015260408601516101c085015260608601516101e0850152608086015161020085015260a086015161022085015260c086015161024085015260e08601516102608501526006604301546102808501526007604301546102a08501526008604301546102c08501526009604301546102e085015260208461030086600060086107d05a03f192505050806115a9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016115a0906129ad565b60405180910390fd5b816000601881106115b657fe5b60200201519250505092915050565b60008060006001860390506000600119861682019050600080600187161461163c576001868401039050611618600082603f81106115ff57fe5b0154600085600202603f811061161157fe5b01546116c6565b60006002600184038161162757fe5b04603f811061163257fe5b0181905550611642565b85830190505b5b8181111561169e5760028103905061167a600082603f811061166157fe5b0154600060018401603f811061167357fe5b01546116c6565b60006002600184038161168957fe5b04603f811061169457fe5b0181905550611643565b600287816116a857fe5b04600260018801816116b657fe5b0494509450505050935093915050565b60007fdec937b7fa8db3de380427a8cc947bfab68514522c3439cfa2e99655098368146000527f30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f00000018284828282088381820984858383098683840909925060005b605a81121561175f57602060002080600052868688838808089350868485099250868488858a8788090909945050600181019050611726565b508484868a8888880808089550505050505092915050565b6040518060400160405280600290602082028038833980820191505090505090565b6040518060800160405280600073ffffffffffffffffffffffffffffffffffffffff168152602001600081526020016060815260200160007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191681525090565b6040518060a00160405280600590602082028038833980820191505090505090565b60405180610100016040528060008152602001600081526020016000815260200160008152602001600081526020016000815260200160008152602001600081525090565b604051806103000160405280601890602082028038833980820191505090505090565b60008135905061188f81612d62565b92915050565b600082601f8301126118a657600080fd5b60026118b96118b482612a7a565b612a4d565b9150818360005b838110156118f057813586016118d68882611a80565b8452602084019350602083019250506001810190506118c0565b5050505092915050565b600082601f83011261190b57600080fd5b600261191e61191982612a9c565b612a4d565b9150818385602084028201111561193457600080fd5b60005b83811015611964578161194a8882611b28565b845260208401935060208301925050600181019050611937565b5050505092915050565b600082601f83011261197f57600080fd5b600461199261198d82612abe565b612a4d565b915081838560208402820111156119a857600080fd5b60005b838110156119d857816119be8882611b28565b8452602084019350602083019250506001810190506119ab565b5050505092915050565b600082601f8301126119f357600080fd5b6009611a06611a0182612ae0565b612a4d565b91508183856020840282011115611a1c57600080fd5b60005b83811015611a4c5781611a328882611b28565b845260208401935060208301925050600181019050611a1f565b5050505092915050565b600081359050611a6581612d79565b92915050565b600081519050611a7a81612d79565b92915050565b600082601f830112611a9157600080fd5b8135611aa4611a9f82612b02565b612a4d565b91508082526020830160208301858383011115611ac057600080fd5b611acb838284612d05565b50505092915050565b600082601f830112611ae557600080fd5b8135611af8611af382612b2e565b612a4d565b91508082526020830160208301858383011115611b1457600080fd5b611b1f838284612d05565b50505092915050565b600081359050611b3781612d90565b92915050565b600080600060608486031215611b5257600080fd5b6000611b6086828701611880565b9350506020611b7186828701611b28565b925050604084013567ffffffffffffffff811115611b8e57600080fd5b611b9a86828701611ad4565b9150509250925092565b60008060008060008060006102e0888a031215611bc057600080fd5b6000611bce8a828b016118fa565b9750506040611bdf8a828b0161196e565b96505060c0611bf08a828b016118fa565b955050610100611c028a828b0161196e565b945050610180611c148a828b01611b28565b9350506101a0611c268a828b016119e2565b9250506102c088013567ffffffffffffffff811115611c4457600080fd5b611c508a828b01611895565b91505092959891949750929550565b60006101208284031215611c7257600080fd5b6000611c80848285016119e2565b91505092915050565b600060208284031215611c9b57600080fd5b6000611ca984828501611a56565b91505092915050565b600060208284031215611cc457600080fd5b6000611cd284828501611a6b565b91505092915050565b6000806101408385031215611cef57600080fd5b6000611cfd85828601611b28565b9250506020611d0e858286016119e2565b9150509250929050565b6000611d248383611fba565b60208301905092915050565b6000611d3c8383611fd8565b60208301905092915050565b6000611d548383612018565b905092915050565b6000611d688383612633565b60208301905092915050565b611d7d81612ccf565b82525050565b611d8c81612c89565b82525050565b611d9b81612b8c565b611da58184612c1a565b9250611db082612b5a565b8060005b83811015611de1578151611dc88782611d18565b9650611dd383612bd9565b925050600181019050611db4565b505050505050565b611df281612b8c565b611dfc8184612c25565b9250611e0782612b5a565b8060005b83811015611e38578151611e1f8782611d30565b9650611e2a83612bd9565b925050600181019050611e0b565b505050505050565b6000611e4b82612b97565b611e558185612c30565b935083602082028501611e6785612b64565b8060005b85811015611ea35784840389528151611e848582611d48565b9450611e8f83612be6565b925060208a01995050600181019050611e6b565b50829750879550505050505092915050565b611ebe81612ba2565b611ec88184612c3b565b9250611ed382612b6e565b8060005b83811015611f04578151611eeb8782611d5c565b9650611ef683612bf3565b925050600181019050611ed7565b505050505050565b611f1581612bad565b611f1f8184612c46565b9250611f2a82612b78565b8060005b83811015611f5b578151611f428782611d5c565b9650611f4d83612c00565b925050600181019050611f2e565b505050505050565b611f6c81612bb8565b611f768184612c51565b9250611f8182612b82565b8060005b83811015611fb2578151611f998782611d5c565b9650611fa483612c0d565b925050600181019050611f85565b505050505050565b611fc381612c9b565b82525050565b611fd281612c9b565b82525050565b611fe181612c9b565b82525050565b6000611ff282612bce565b611ffc8185612c6d565b935061200c818560208601612d14565b80840191505092915050565b600061202382612bc3565b61202d8185612c5c565b935061203d818560208601612d14565b61204681612d51565b840191505092915050565b600061205c82612bc3565b6120668185612c6d565b9350612076818560208601612d14565b80840191505092915050565b600061208f601883612c78565b91507f6e756c6c696669657220696e646578206f766572666c6f7700000000000000006000830152602082019050919050565b60006120cf603783612c78565b91507f496e76616c6964206e756c6c69666965723a2054686973206e756c6c6966696560008301527f722068617320616c7265616479206265656e20757365640000000000000000006020830152604082019050919050565b6000612135601e83612c78565b91507f767075625f696e2072657475726e207472616e73666572206661696c656400006000830152602082019050919050565b6000612175601883612c78565b91507f767075625f6f7574207472616e73666572206661696c656400000000000000006000830152602082019050919050565b60006121b5602783612c78565b91507f4d65726b6c6520747265652066756c6c3a2043616e6e6f7420617070656e642060008301527f616e796d6f7265000000000000000000000000000000000000000000000000006020830152604082019050919050565b600061221b603083612c78565b91507f6e756c6c6966696572207772697474656e20696e20646966666572656e74207260008301527f6573696475616c2062697420662e652e000000000000000000000000000000006020830152604082019050919050565b6000612281602583612c78565b91507f496e76616c696420726f6f743a205468697320726f6f7420646f65736e27742060008301527f65786973740000000000000000000000000000000000000000000000000000006020830152604082019050919050565b60006122e7604983612c78565b91507f496e76616c696420687369673a2054686973206873696720646f6573206e6f7460008301527f20636f72726573706f6e6420746f207468652068617368206f6620766b20616e60208301527f6420746865206e667300000000000000000000000000000000000000000000006040830152606082019050919050565b6000612373602283612c78565b91507f496e707574206c656e67746820646966666572732066726f6d2065787065637460008301527f65640000000000000000000000000000000000000000000000000000000000006020830152604082019050919050565b60006123d9603383612c78565b91507f496e76616c69642070726f6f663a20556e61626c6520746f207665726966792060008301527f7468652070726f6f6620636f72726563746c79000000000000000000000000006020830152604082019050919050565b600061243f602a83612c78565b91507f57726f6e67206d73672e76616c75653a2056616c75652070616964206973206e60008301527f6f7420636f7272656374000000000000000000000000000000000000000000006020830152604082019050919050565b60006124a5601c83612c78565b91507f496e707574206973206e6f7420696e207363616c6172206669656c64000000006000830152602082019050919050565b60006124e5603b83612c78565b91507f496e76616c6964207369676e61747572653a20556e61626c6520746f2076657260008301527f69667920746865207369676e617475726520636f72726563746c7900000000006020830152604082019050919050565b600061254b600083612c6d565b9150600082019050919050565b6000612565603783612c78565b91507f43616c6c20746f20626e3235364164642c20626e3235365363616c61724d756c60008301527f206f7220626e32353650616972696e67206661696c65640000000000000000006020830152604082019050919050565b60006125cb603983612c78565b91507f43616c6c20746f2074686520626e323536416464206f7220626e32353653636160008301527f6c61724d756c20707265636f6d70696c6564206661696c6564000000000000006020830152604082019050919050565b61262d81612cc5565b82525050565b61263c81612cc5565b82525050565b61265361264e82612cc5565b612d47565b82525050565b60006126658285611de9565b6040820191506126758284611f0c565b6080820191508190509392505050565b60006126918284611fe7565b915081905092915050565b60006126a78261253e565b9150819050919050565b60006126bd828a612642565b6020820191506126cd8289612051565b91506126d98288612051565b91506126e58287611eb5565b6040820191506126f58286611f0c565b6080820191506127058285611eb5565b6040820191506127158284611f63565b6101208201915081905098975050505050505050565b60006020820190506127406000830184611d83565b92915050565b600060608201905061275b6000830186611d74565b6127686020830185611d83565b6127756040830184612624565b949350505050565b60006040820190506127926000830185611d74565b61279f6020830184612624565b9392505050565b60006020820190506127bb6000830184611fc9565b92915050565b600060c0820190506127d66000830187611fc9565b6127e36020830186611d92565b6127f06060830185611d92565b81810360a08301526128028184611e40565b905095945050505050565b6000602082019050818103600083015261282681612082565b9050919050565b60006020820190508181036000830152612846816120c2565b9050919050565b6000602082019050818103600083015261286681612128565b9050919050565b6000602082019050818103600083015261288681612168565b9050919050565b600060208201905081810360008301526128a6816121a8565b9050919050565b600060208201905081810360008301526128c68161220e565b9050919050565b600060208201905081810360008301526128e681612274565b9050919050565b60006020820190508181036000830152612906816122da565b9050919050565b6000602082019050818103600083015261292681612366565b9050919050565b60006020820190508181036000830152612946816123cc565b9050919050565b6000602082019050818103600083015261296681612432565b9050919050565b6000602082019050818103600083015261298681612498565b9050919050565b600060208201905081810360008301526129a6816124d8565b9050919050565b600060208201905081810360008301526129c681612558565b9050919050565b600060208201905081810360008301526129e6816125be565b9050919050565b6000604082019050612a026000830185612624565b612a0f6020830184612624565b9392505050565b6000606082019050612a2b6000830186612624565b612a386020830185612624565b612a456040830184612624565b949350505050565b6000604051905081810181811067ffffffffffffffff82111715612a7057600080fd5b8060405250919050565b600067ffffffffffffffff821115612a9157600080fd5b602082029050919050565b600067ffffffffffffffff821115612ab357600080fd5b602082029050919050565b600067ffffffffffffffff821115612ad557600080fd5b602082029050919050565b600067ffffffffffffffff821115612af757600080fd5b602082029050919050565b600067ffffffffffffffff821115612b1957600080fd5b601f19601f8301169050602081019050919050565b600067ffffffffffffffff821115612b4557600080fd5b601f19601f8301169050602081019050919050565b6000819050919050565b6000819050919050565b6000819050919050565b6000819050919050565b6000819050919050565b600060029050919050565b600060029050919050565b600060029050919050565b600060049050919050565b600060099050919050565b600081519050919050565b600081519050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b6000602082019050919050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b6000612c9482612ca5565b9050919050565b6000819050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b6000612cda82612ce1565b9050919050565b6000612cec82612cf3565b9050919050565b6000612cfe82612ca5565b9050919050565b82818337600083830152505050565b60005b83811015612d32578082015181840152602081019050612d17565b83811115612d41576000848401525b50505050565b6000819050919050565b6000601f19601f8301169050919050565b612d6b81612c89565b8114612d7657600080fd5b50565b612d8281612c9b565b8114612d8d57600080fd5b50565b612d9981612cc5565b8114612da457600080fd5b5056fea365627a7a72315820581195eb613966cd593b726868fc28cf68f8daa35097a7bd66193af259e0d6006c6578706572696d656e74616cf564736f6c63430005110040"

    client = BcosClient()
    mixerTransactionRecipient = client.sendRawTransactionGetReceipt("", abi5, None, constructArgs, bin5, 30000000, 15)
    mixer_address = mixerTransactionRecipient['contractAddress']
    print(f"deploy: mixer_address={mixer_address}")
    #mixer_instance = Groth16Mixer(address)


if __name__ == '__main__':
    deploy()
