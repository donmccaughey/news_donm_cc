@import Foundation;

#import "JSONDeserialized.h"


NS_ASSUME_NONNULL_BEGIN


@interface Source : JSONDeserialized

@property (readonly) NSUInteger count;
@property (readonly) NSString *siteID;
@property (readonly) NSURL *url;

- (instancetype)init NS_UNAVAILABLE;

- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;

@end


NS_ASSUME_NONNULL_END
