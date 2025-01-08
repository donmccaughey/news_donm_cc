#import "NewsViewController.h"

#import "AppDelegate.h"
#import "Item.h"
#import "ItemCell.h"
#import "News.h"
#import "NewsAPI.h"


static NSString *itemCellName = @"ItemCell";


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
    [_tableView registerNib:[UINib nibWithNibName:itemCellName bundle:nil]
     forCellReuseIdentifier:itemCellName];
    
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(newsAPIDidFetchNews:)
                                                 name:NewsAPIDidFetchNewsNotification
                                               object:nil];
}


- (UITableViewCell *)tableView:(UITableView *)tableView
         cellForRowAtIndexPath:(NSIndexPath *)indexPath;
{
    ItemCell *cell = [tableView dequeueReusableCellWithIdentifier:itemCellName];
    cell.item = [self.news itemAtIndex:indexPath.row];
    return cell;
}


- (void)      tableView:(UITableView *)tableView
didSelectRowAtIndexPath:(NSIndexPath *)indexPath;
{
    Item *cell = [tableView cellForRowAtIndexPath:indexPath];
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    // TODO: show detail view for cell.item
}


- (NSInteger)tableView:(UITableView *)tableView
 numberOfRowsInSection:(NSInteger)section;
{
    return self.news.count;
}


@end
