@import Foundation;


@class Item;
@class NewsPage;
@class NewsRange;


NS_ASSUME_NONNULL_BEGIN


@interface News : NSObject

@property (readonly) NSUInteger count;
@property NSMutableOrderedSet<Item *> *items;
@property (readonly) NewsRange *itemsRange;
@property NSDate *modified;
@property NSUInteger newestItemSeqID;
@property NSUInteger oldestItemSeqID;

- (void)addNewsPage:(NewsPage *)newsPage;

- (nullable Item *)itemAtIndex:(NSInteger)index;

@end


NS_ASSUME_NONNULL_END
