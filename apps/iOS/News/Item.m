#import "Item.h"

#import "Errors.h"
#import "Source.h"


@implementation Item


- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;
{
    self = [super init];
    if ( ! self) return nil;
    
    _created = [self date:@"created" fromJSON:json];
    _modfied = [self date:@"modified" fromJSON:json];
    _seqID = [self unsignedInteger:@"seq_id" fromJSON:json];
    _sources = [self array:@"sources" ofClass:[Source class] fromJSON:json];
    _title = [self string:@"title" fromJSON:json];
    _url = [self url:@"url" fromJSON:json];
    _urlIdentity = [self string:@"url_identity" fromJSON:json];
    
    if (self.error) {
        if (error) *error = self.error;
    }
    
    if ( ! _sources.count) {
        if (error) *error = [NSError errorWithDomain:NewsErrorDomain
                                                code:NewsErrorInvalidJSON
                                            userInfo:nil];
        return nil;
    }

    return self;
}


- (BOOL)isEqual:(id)object;
{
    if (self == object) return YES;
    if ( ! [object isKindOfClass:[Item class]]) return NO;
    Item *item = object;
    return _seqID == item->_seqID;
}


- (NSUInteger)hash;
{
    return _seqID;
}


@end
