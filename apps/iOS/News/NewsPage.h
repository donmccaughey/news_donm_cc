@import Foundation;

#import "JSONDeserialized.h"


@class Item;
@class NewsRange;


NS_ASSUME_NONNULL_BEGIN


@interface NewsPage : JSONDeserialized

@property (readonly) NSUInteger firstItemIndex;
@property (nullable, readonly) NSURL *firstURL;
@property (readonly) NSArray<Item *> *items;
@property (readonly) NSUInteger itemsPerPage;
@property (readonly) NewsRange *itemsRange;
@property (nullable, readonly) NSURL *lastURL;
@property (readonly) NSDate *modified;
@property (readonly) NSUInteger newestItemSeqID;
@property (nullable, readonly) NSURL *nextURL;
@property (readonly) NSUInteger oldestItemSeqID;
@property (readonly) NSUInteger pageIndex;
@property (nullable, readonly) NSURL *previousURL;
@property (readonly) NSUInteger totalItems;
@property (readonly) NSUInteger totalPages;
@property (readonly) NSString *version;

- (instancetype)init NS_UNAVAILABLE;

- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;

@end


NS_ASSUME_NONNULL_END
