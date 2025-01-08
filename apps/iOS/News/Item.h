@import Foundation;

#import "JSONDeserialized.h"


@class Source;


NS_ASSUME_NONNULL_BEGIN


@interface Item : JSONDeserialized

@property (readonly) NSDate *created;
@property (readonly) NSDate *modfied;
@property (readonly) NSUInteger seqID;
@property (readonly) NSArray<NSString *> *siteIDs;
@property (readonly) NSArray<Source *> *sources;
@property (readonly) NSString *title;
@property (readonly) NSURL *url;
@property (readonly) NSString *urlIdentity;

- (instancetype)init NS_UNAVAILABLE;

- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;

@end


NS_ASSUME_NONNULL_END
