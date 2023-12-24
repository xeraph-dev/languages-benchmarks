import CryptoKit
import Foundation

let zeros = Array(repeating: UInt8(0), count: 3)

var hash = Insecure.MD5()
hash.update(data: "yzbqklnj".data(using: .utf8)!)

for i in 0... {
    var hash = hash
    hash.update(data: i.description.data(using: .utf8)!)
    if hash.finalize().starts(with: zeros) {
        print(i)
        break
    }
}
