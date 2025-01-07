#import "NewsPage.h"

#import "Errors.h"
#import "Item.h"
#import "NewsRange.h"


@implementation NewsPage


- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;
{
    self = [super init];
    if ( ! self) return nil;
    
    _firstItemIndex = [self unsignedInteger:@"first_item_index" fromJSON:json];
    _firstURL = [self nullableURL:@"first_url" fromJSON:json];
    _items = [self array:@"items" ofClass:[Item class] fromJSON:json];
    _itemsPerPage = [self unsignedInteger:@"items_per_page" fromJSON:json];
    _lastURL = [self nullableURL:@"last_url" fromJSON:json];
    _modified = [self date:@"modified" fromJSON:json];
    _newestItemSeqID = [self unsignedInteger:@"newest_item_seq_id" fromJSON:json];
    _nextURL = [self nullableURL:@"next_url" fromJSON:json];
    _oldestItemSeqID = [self unsignedInteger:@"oldest_item_seq_id" fromJSON:json];
    _previousURL = [self nullableURL:@"previous_url" fromJSON:json];
    _totalItems = [self unsignedInteger:@"total_items" fromJSON:json];
    _totalPages = [self unsignedInteger:@"total_pages" fromJSON:json];
    _version = [self string:@"version" fromJSON:json];
    
    if (self.error) {
        if (error) *error = self.error;
        return nil;
    }
    
    if ( ! _items.count) {
        if (error) *error = [NSError errorWithDomain:NewsErrorDomain
                                                code:NewsErrorInvalidJSON
                                            userInfo:nil];
        return nil;
    }

    return self;
}


- (NewsRange *)itemsRange;
{
    return [[NewsRange alloc] initWithNewestSeqID:_items.firstObject.seqID
                                   andOldestSeqID:_items.lastObject.seqID];
}


@end
