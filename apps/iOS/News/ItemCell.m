#import "ItemCell.h"

#import "Item.h"
#import "Source.h"


@implementation ItemCell
{
    Item *_item;
}


- (Item *)item;
{
    return _item;
}


- (void )setItem:(Item *)item;
{
    _item = item;
    if (_item) {
        _title.text = _item.title;
        _details.text = [self detailsString];
    } else {
        _title.text = @"(news item)";
        _details.text = @"";
    }
}


- (NSString *)detailsString;{
    if ( ! _item) return @"";
    NSMutableArray *parts = [NSMutableArray arrayWithObject:_item.urlIdentity];
    [parts addObjectsFromArray:_item.siteIDs];
    [parts addObject:_item.created.description];
    return [parts componentsJoinedByString:@" — "];
}


@end
