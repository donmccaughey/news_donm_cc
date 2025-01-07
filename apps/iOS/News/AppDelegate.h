@import UIKit;


@class News;
@class NewsAPI;


@interface AppDelegate : UIResponder<UIApplicationDelegate>

@property News *news;
@property NewsAPI *newsAPI;
@property (strong, nonatomic) UIWindow *window;

- (void)newsAPIDidFail:(NSNotification *)notification;

- (void)newsAPIDidFetchNews:(NSNotification *)notification;

@end
