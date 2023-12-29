const std = @import("std");
const md5 = std.crypto.hash.Md5;

fn collide(str: []const u8, comptime salt: u32, comptime start: comptime_int, comptime takebit: bool) !void {
    var output: [md5.digest_length]u8 = undefined;
    var buf: [20]u8 = undefined;
    var hashfn = md5.init(.{});
    hashfn.update(str);

    for (0..salt) |i| {
        var tmphash = hashfn;
        const salty = try std.fmt.bufPrint(&buf, "{d}", .{i});
        tmphash.update(salty);
        tmphash.final(&output);

        if (computeStartsWithCmp(&output, start, takebit)) {
            try std.io.getStdOut().writer().print("{any} - {d}\n", .{ std.fmt.fmtSliceHexLower(&output), i });
            break;
        }
    }
}

inline fn computeStartsWithCmp(str: []const u8, comptime zeroes: usize, takebit: bool) bool {
    var valid: bool = false;

    var zeros: [zeroes - 1]u8 = undefined;
    @memset(&zeros, 0);

    if (std.mem.startsWith(u8, str[0..zeroes], &zeros)) {
        valid = true;
        if (takebit) {
            switch (str[0..zeroes].*[0 .. str[0..zeroes].len - 1]) {
                inline 0x1...0x8 => valid = true,
                inline else => valid = false,
            }
        }
    }

    return valid;
}

pub fn main() !void {
    const salt = std.math.maxInt(u32);
    @setEvalBranchQuota(salt);
    try collide("yzbqklnj", salt, 4, false);
}
