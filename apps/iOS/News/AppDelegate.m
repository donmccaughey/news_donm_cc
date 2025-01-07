#import "AppDelegate.h"

#import "News.h"
#import "NewsAPI.h"
#import "NewsPage.h"
#import "NewsRange.h"
#import "NewsViewController.h"


@implementation AppDelegate


- (instancetype)init;
{
    self = [super init];
    if ( ! self) return nil;
    
    _news = [News new];
    _newsAPI = [NewsAPI new];

    return self;
}

- (void)dealloc;
{
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}


- (BOOL)          application:(UIApplication *)application
didFinishLaunchingWithOptions:(NSDictionary *)launchOptions;
{
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    self.window.rootViewController = [NewsViewController new];
    [self.window makeKeyAndVisible];
    
    return YES;
}


- (BOOL)           application:(UIApplication *)application
willFinishLaunchingWithOptions:(NSDictionary<UIApplicationLaunchOptionsKey,id> *)launchOptions;
{

    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(newsAPIDidFail:)
                                                 name:NewsAPIDidFailNotification
                                               object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(newsAPIDidFetchNews:)
                                                 name:NewsAPIDidFetchNewsNotification
                                               object:nil];
    
    [_newsAPI startFetchingNews:_news];
    
    return YES;
}


- (void)newsAPIDidFail:(NSNotification *)notification;
{
    NSError *error = notification.userInfo[ErrorKey];
    NSLog(@"News API did fail: %@", error);
}


- (void)newsAPIDidFetchNews:(NSNotification *)notification;
{
    NewsPage *newsPage = notification.userInfo[NewsPageKey];
    NSLog(@"Fetched %lu news items in range %@", newsPage.items.count, newsPage.itemsRange);
}


@end
