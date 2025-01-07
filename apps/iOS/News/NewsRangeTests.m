@import XCTest;

#import "NewsRange.h"


@interface NewsRangeTests : XCTestCase
@end


@implementation NewsRangeTests


- (void)testIsDisjointWith;
{
    NewsRange *range1_3 = [[NewsRange alloc] initWithNewestSeqID:3 andOldestSeqID:1];
    NewsRange *range4_5 = [[NewsRange alloc] initWithNewestSeqID:5 andOldestSeqID:4];
    NewsRange *range6_8 = [[NewsRange alloc] initWithNewestSeqID:8 andOldestSeqID:6];

    XCTAssertTrue([range1_3 isDisjointWith:range4_5]);
    XCTAssertTrue([range4_5 isDisjointWith:range1_3]);
    
    XCTAssertTrue([range4_5 isDisjointWith:range6_8]);
    XCTAssertTrue([range6_8 isDisjointWith:range4_5]);
    
    NewsRange *range1_4 = [[NewsRange alloc] initWithNewestSeqID:4 andOldestSeqID:1];
    NewsRange *range5_8 = [[NewsRange alloc] initWithNewestSeqID:8 andOldestSeqID:5];
    
    XCTAssertFalse([range1_4 isDisjointWith:range4_5]);
    XCTAssertFalse([range4_5 isDisjointWith:range1_4]);

    XCTAssertFalse([range4_5 isDisjointWith:range5_8]);
    XCTAssertFalse([range5_8 isDisjointWith:range4_5]);
}


@end
