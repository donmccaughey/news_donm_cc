#import "NewsViewController.h"

#import "AppDelegate.h"
#import "Item.h"
#import "News.h"
#import "NewsAPI.h"


@implementation NewsViewController


- (instancetype)init;
{
    self = [super initWithNibName:nil bundle:nil];
    if ( ! self) return nil;
    
    return self;
}


- (void)dealloc;
{
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}


- (News *)news;
{
    AppDelegate *appDelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    return appDelegate.news;
}


- (void)newsAPIDidFetchNews:(NSNotification *)notification;
{
    // TODO: reload intelligently, refresh data in affected cells
    [_tableView reloadData];
}


- (void)viewDidLoad;
{
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(newsAPIDidFetchNews:)
                                                 name:NewsAPIDidFetchNewsNotification
                                               object:nil];
}


- (UITableViewCell *)tableView:(UITableView *)tableView
         cellForRowAtIndexPath:(NSIndexPath *)indexPath;
{
    static NSString *cellIdentifier = @"NewsCell";
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellIdentifier];
    if ( ! cell) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleSubtitle
                                      reuseIdentifier:cellIdentifier];
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
        cell.selectionStyle = UITableViewCellSelectionStyleDefault;
        cell.textLabel.adjustsFontSizeToFitWidth = YES;
        cell.textLabel.minimumScaleFactor = 0.8;
    }
    
    Item *item = [self.news itemAtIndex:indexPath.row];
    if (item) {
        cell.textLabel.text = item.title;
        cell.detailTextLabel.text = item.url.description;
    } else {
        cell.textLabel.text = @"(news item)";
        cell.detailTextLabel.text = @"";
    }
    
    return cell;
}


- (NSInteger)tableView:(UITableView *)tableView
 numberOfRowsInSection:(NSInteger)section;
{
    NSLog(@"self.news.count = %lu", self.news.count);
    return self.news.count;
}


@end
