const std = @import("std");
const md5 = std.crypto.hash.Md5;

fn collide(allocator: std.mem.Allocator, str: []const u8, comptime salt: u32, comptime start: usize, takebit: bool) !void {
    var output: [md5.digest_length]u8 = undefined;
    var hashfn = md5.init(.{});
    hashfn.update(str);

    for (0..salt) |i| {
        var tmphash = hashfn;
        tmphash.update((try std.fmt.allocPrint(allocator, "{d}", .{i})));
        tmphash.final(&output);

        if (computeStartsWithCmp(&output, start, takebit)) {
            try std.io.getStdOut().writer().print("{any} - {d}\n", .{ std.fmt.fmtSliceHexLower(&output), i });
            break;
        }
    }
}

inline fn computeStartsWithCmp(str: []const u8, comptime zeroes: usize, takebit: bool) bool {
    var arr = std.mem.sliceAsBytes(str[0..zeroes]);
    var valid: bool = false;

    var zeros: [zeroes - 1]u8 = undefined;
    @memset(&zeros, 0);

    if (std.mem.startsWith(u8, arr, &zeros)) {
        valid = true;
        if (takebit) {
            switch (arr[arr.len - 1]) {
                0x1...0x09 => valid = true,
                else => valid = false,
            }
        }
    }

    return valid;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    var allocator = arena.allocator();
    @setEvalBranchQuota(std.math.maxInt(u32));
    try collide(allocator, "yzbqklnj", std.math.maxInt(u32), 3, true);
}
