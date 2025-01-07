#import "NewsAPI.h"

#import "Errors.h"
#import "News.h"
#import "NewsPage.h"
#import "NewsRange.h"


NSNotificationName NewsAPIDidFetchNewsNotification = @"NewsAPIDidFetchNews";
NSNotificationName NewsAPIDidFailNotification = @"NewsAPIDidFail";
NSString *const ErrorKey = @"Error";
NSString *const NewsPageKey = @"NewsPage";


static int64_t const apiCooloff = (int64_t)1 * NSEC_PER_SEC;


@implementation NewsAPI
{
    NSURLSession *_session;
}


- (instancetype)init;
{
    self = [super init];
    if ( ! self) return nil;
    
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    _session = [NSURLSession sessionWithConfiguration:configuration];
    
    return self;
}


- (void)dealloc;
{
    [_session invalidateAndCancel];
}


- (void)startFetchingNews:(News *)news;
{
    NSURL *page1 = [NSURL URLWithString:@"https://news.donm.cc/"];
    [self startFetchingNews:news
                      atURL:page1];
}


- (void)startFetchingNews:(News *)news
                    atURL:(NSURL *)url;
{
    NSLog(@"Fetching news page %@", url);
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    [request setValue:@"application/json" forHTTPHeaderField:@"Accept"];
    
    NSURLSessionDataTask *task = [_session dataTaskWithRequest:request
                                             completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [[NSNotificationCenter defaultCenter] postNotificationName:NewsAPIDidFailNotification
                                                                    object:self
                                                                  userInfo:@{ ErrorKey: error }];
            });
            // TODO: retry
            return;
        }
        
        NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *)response;
        if (httpResponse.statusCode != 200) {
            NSError *statusError = [NSError errorWithDomain:NewsErrorDomain
                                                       code:httpResponse.statusCode
                                                   userInfo:@{NSLocalizedDescriptionKey: @"HTTP Error"}];
            dispatch_async(dispatch_get_main_queue(), ^{
                [[NSNotificationCenter defaultCenter] postNotificationName:NewsAPIDidFailNotification
                                                                    object:self
                                                                  userInfo:@{ ErrorKey: statusError }];
            });
            // TODO: retry
            return;
        }
        
        NSError *jsonError;
        NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data
                                                             options:0
                                                               error:&jsonError];
        if ( ! json || ! [json isKindOfClass:[NSDictionary class]]) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [[NSNotificationCenter defaultCenter] postNotificationName:NewsAPIDidFailNotification
                                                                    object:self
                                                                  userInfo:@{ ErrorKey: jsonError }];
            });
            return;
        }
        
        NewsPage *newsPage = [[NewsPage alloc] initWithJSON:json error:&jsonError];
        if ( ! newsPage) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [[NSNotificationCenter defaultCenter] postNotificationName:NewsAPIDidFailNotification
                                                                    object:self
                                                                  userInfo:@{ ErrorKey: jsonError }];
            });
            return;
        }

        dispatch_async(dispatch_get_main_queue(), ^{
            BOOL shouldFetchMore = [newsPage.itemsRange isDisjointWith:news.itemsRange];
            [news addNewsPage:newsPage];
            
            [[NSNotificationCenter defaultCenter] postNotificationName:NewsAPIDidFetchNewsNotification
                                                                object:self
                                                              userInfo:@{ NewsPageKey: newsPage }];
            
            if (shouldFetchMore && newsPage.nextURL) {
                dispatch_after(dispatch_time(DISPATCH_TIME_NOW, apiCooloff), dispatch_get_main_queue(), ^{
                    [self startFetchingNews:news
                                      atURL:newsPage.nextURL];
                });
            }
        });
    }];
    
    [task resume];
}


@end
