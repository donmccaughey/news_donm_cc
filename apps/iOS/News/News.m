#import "News.h"

#import "Item.h"
#import "NewsPage.h"
#import "NewsRange.h"


@implementation News


- (instancetype)init;
{
    self = [super init];
    if ( ! self) return nil;
    
    _items = [NSMutableOrderedSet new];
    
    return self;
}


- (NSUInteger)count;
{
    if ( ! _items.count) return 0;
    return _newestItemSeqID - _oldestItemSeqID + 1;
}


- (NewsRange *)itemsRange;
{
    return [[NewsRange alloc] initWithNewestSeqID:_items.firstObject.seqID
                                   andOldestSeqID:_items.lastObject.seqID];
}


- (void)addNewsPage:(NewsPage *)newsPage;
{
    _modified = newsPage.modified;
    _newestItemSeqID = newsPage.newestItemSeqID;
    _oldestItemSeqID = newsPage.oldestItemSeqID;
    [_items addObjectsFromArray:newsPage.items];
    [_items sortUsingDescriptors:@[
        [NSSortDescriptor sortDescriptorWithKey:@"seqID" ascending:NO],
    ]];
}


- (nullable Item *)itemAtIndex:(NSInteger)index;
{
    return (index < _items.count) ? _items[index] : nil;
}


@end
