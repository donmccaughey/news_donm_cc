@import Foundation;



NS_ASSUME_NONNULL_BEGIN


@interface NewsRange : NSObject

@property (readonly) NSUInteger newestSeqID;
@property (readonly) NSUInteger oldestSeqID;

- (instancetype)init NS_UNAVAILABLE;

- (instancetype)initWithNewestSeqID:(NSUInteger)newestSeqID
                     andOldestSeqID:(NSUInteger)oldestSeqID;

- (BOOL)isDisjointWith:(NewsRange *)other;

@end


NS_ASSUME_NONNULL_END
