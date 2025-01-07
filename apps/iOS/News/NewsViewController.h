@import UIKit;


@class News;


@interface NewsViewController : UIViewController<UITableViewDataSource, UITableViewDelegate>

@property (readonly) News *news;
@property (weak) IBOutlet UITableView *tableView;

- (void)newsAPIDidFetchNews:(NSNotification *)notification;

@end
