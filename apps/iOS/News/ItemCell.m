#import "ItemCell.h"

#import "Item.h"


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
        _urlIdentity.text = _item.urlIdentity;
    } else {
        _title.text = @"(news item)";
        _urlIdentity.text = @"";
    }
}




@end
