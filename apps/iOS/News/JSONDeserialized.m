#import "JSONDeserialized.h"

#import "Errors.h"
#import "NSDate+ISO8601.h"


@implementation JSONDeserialized


- (NSArray *)array:(NSString *)name
           ofClass:(Class<JSONDeserializable>)cls
          fromJSON:(NSDictionary<NSString *, id> *)json;
{
    id value = json[name];
    if (value && [value isKindOfClass:[NSArray class]]) {
        NSArray *array = value;
        NSMutableArray *objects = [NSMutableArray new];
        for (id value in array) {
            if ( ! [value isKindOfClass:[NSDictionary class]]) {
                break;
            }
            NSDictionary *json = value;
            id source = [[cls alloc] initWithJSON:json error:nil];
            if ( ! source) {
                break;
            }
            [objects addObject:source];
        }
        return objects;
    }
    
    NSString *message = [NSString stringWithFormat:@"Array of %@ not found for '%@' in %@",
                         cls.description, name, json];
    self.error = [NSError errorWithDomain:NewsErrorDomain
                                     code:NewsErrorInvalidJSON
                                 userInfo:@{ NSLocalizedDescriptionKey: message }];
    return nil;
}


- (NSDate *)date:(NSString *)name
        fromJSON:(NSDictionary<NSString *, id> *)json;
{
    NSString *string = [self string:name fromJSON:json];
    if (string) {
        NSDate *date = [NSDate dateFromISO8601String:string];
        if (date) return date;
    }
    
    NSString *message = [NSString stringWithFormat:@"Date value not found for '%@' in %@", name, json];
    self.error = [NSError errorWithDomain:NewsErrorDomain
                                     code:NewsErrorInvalidJSON
                                 userInfo:@{ NSLocalizedDescriptionKey: message }];
    return nil;
}


- (NSURL *)nullableURL:(NSString *)name
              fromJSON:(NSDictionary<NSString *, id> *)json;
{
    id value = json[name];
    if (value == [NSNull null]) return nil;
    return [self url:name fromJSON:json];
}


- (NSString *)string:(NSString *)name
            fromJSON:(NSDictionary<NSString *, id> *)json;
{
    id value = json[name];
    if (value && [value isKindOfClass:[NSString class]]) {
        NSString *string = value;
        return string;
    }
    
    NSString *message = [NSString stringWithFormat:@"String value not found for '%@' in %@", name, json];
    self.error = [NSError errorWithDomain:NewsErrorDomain
                                     code:NewsErrorInvalidJSON
                                 userInfo:@{ NSLocalizedDescriptionKey: message }];
    return nil;
}


- (NSUInteger)unsignedInteger:(NSString *)name
                     fromJSON:(NSDictionary<NSString *, id> *)json;
{
    id value = json[name];
    if (value && [value isKindOfClass:[NSNumber class]]) {
        NSNumber *number = value;
        return number.unsignedIntegerValue;
    }
    
    NSString *message = [NSString stringWithFormat:@"Unsigned integer value not found for '%@' in %@", name, json];
    self.error = [NSError errorWithDomain:NewsErrorDomain
                                     code:NewsErrorInvalidJSON
                                 userInfo:@{ NSLocalizedDescriptionKey: message }];
    return 0;
}


- (NSURL *)url:(NSString *)name
      fromJSON:(NSDictionary<NSString *, id> *)json;
{
    NSString *string = [self string:name fromJSON:json];
    if (string) {
        NSURL *url = [NSURL URLWithString:string];
        if (url) return url;
    }

    NSString *message = [NSString stringWithFormat:@"URL value not found for '%@' in %@", name, json];
    self.error = [NSError errorWithDomain:NewsErrorDomain
                                     code:NewsErrorInvalidJSON
                                 userInfo:@{ NSLocalizedDescriptionKey: message }];
    return nil;
}


@end
