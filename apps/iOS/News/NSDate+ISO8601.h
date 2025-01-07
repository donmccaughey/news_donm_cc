@import Foundation;


NS_ASSUME_NONNULL_BEGIN


@interface NSDate (ISO8601)

+ (nullable NSDate *)dateFromISO8601String:(NSString *)string;

@end


NS_ASSUME_NONNULL_END
