@import UIKit;


@class Item;


NS_ASSUME_NONNULL_BEGIN


@interface ItemCell : UITableViewCell

@property Item *item;
@property (weak) IBOutlet UILabel *title;
@property (weak) IBOutlet UILabel *urlIdentity;

@end


NS_ASSUME_NONNULL_END
