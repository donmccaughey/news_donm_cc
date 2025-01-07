#import "NSDate+ISO8601.h"


@implementation NSDate (ISO8601)


+ (nullable NSDate *)dateFromISO8601String:(NSString *)string;
{
    if ( ! string) return nil;
    return [[self ISO8601DateFormatter] dateFromString:string];
}


+ (NSDateFormatter *)ISO8601DateFormatter;
{
    static NSDateFormatter *formatter;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        formatter = [NSDateFormatter new];
        formatter.locale = [NSLocale localeWithLocaleIdentifier:@"C_POSIX"];
        formatter.dateFormat = @"yyyy-MM-dd'T'HH:mm:ss.SSSSSSZZZZZ";
        formatter.timeZone = [NSTimeZone timeZoneForSecondsFromGMT:0];
    });
    return formatter;
}


@end
