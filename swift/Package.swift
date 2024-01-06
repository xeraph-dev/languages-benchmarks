// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "languages-benchmarks",
    platforms: [.macOS(.v10_15)],
    targets: [
        .executableTarget(name: "aoc-year2015-day4"),
        .executableTarget(name: "aoc-year2020-day15")
    ]
)
