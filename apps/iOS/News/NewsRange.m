#import "NewsRange.h"


@implementation NewsRange


- (instancetype)initWithNewestSeqID:(NSUInteger)newestSeqID
                     andOldestSeqID:(NSUInteger)oldestSeqID;
{
    NSAssert(newestSeqID >= oldestSeqID,
             @"Expedted newest %lu to be more than oldest %lu",
             newestSeqID, oldestSeqID);
    
    self = [super init];
    if ( ! self) return nil;
    
    _newestSeqID = newestSeqID;
    _oldestSeqID = oldestSeqID;
    
    return self;
}


- (BOOL)isDisjointWith:(NewsRange *)other;
{
    return _newestSeqID < other->_oldestSeqID
        || other->_newestSeqID < _oldestSeqID;
}


- (NSString *)description;
{
    return [NSString stringWithFormat:@"[%lu, %lu]", _oldestSeqID, _newestSeqID];
}


@end
