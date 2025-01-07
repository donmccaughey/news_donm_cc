@import Foundation;


@class News;


NS_ASSUME_NONNULL_BEGIN


extern NSNotificationName NewsAPIDidFetchNewsNotification;
extern NSNotificationName NewsAPIDidFailNotification;
extern NSString *const ErrorKey;
extern NSString *const NewsPageKey;


@interface NewsAPI : NSObject

- (void)startFetchingNews:(News *)news;

- (void)startFetchingNews:(News *)news
                    atURL:(NSURL *)url;

@end


NS_ASSUME_NONNULL_END
