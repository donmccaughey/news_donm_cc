#import "Source.h"

#import "Errors.h"


@implementation Source


- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;
{
    self = [super init];
    if ( ! self) return nil;
    
    _count = [self unsignedInteger:@"count" fromJSON:json];
    _siteID = [self string:@"site_id" fromJSON:json];
    _url = [self url:@"url" fromJSON:json];
    
    if (self.error) {
        if (error) *error = self.error;
        return nil;
    }

    return self;
}


@end
