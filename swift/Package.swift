// swift-tools-version: 5.9
import PackageDescription

let package = Package(
  name: "languages-benchmarks",
  platforms: [.macOS(.v10_15)],
  dependencies: [
    .package(url: "https://github.com/apple/swift-atomics.git", .upToNextMajor(from: "1.2.0")),
    .package(url: "https://github.com/apple/swift-crypto.git", .upToNextMajor(from: "3.0.0")),
  ],
  targets: [
    .executableTarget(
      name: "aoc-year2015-day4-xeraph-dev",
      dependencies: [
        .product(name: "Atomics", package: "swift-atomics"),
        .product(name: "Crypto", package: "swift-crypto"),
      ],
      path: "Sources/aoc-year2015-day4/xeraph-dev"
    ),
    .executableTarget(
      name: "aoc-year2020-day15-xeraph-dev",
      path: "Sources/aoc-year2020-day15/xeraph-dev"
    ),
  ]
)
