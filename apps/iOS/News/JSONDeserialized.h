@import Foundation;


NS_ASSUME_NONNULL_BEGIN


@protocol JSONDeserializable<NSObject>

+ (instancetype)alloc;

- (nullable instancetype)initWithJSON:(NSDictionary<NSString *, id> *)json
                                error:(NSError **)error;

@end


@interface JSONDeserialized<JSONDeserializable> : NSObject

@property NSError *error;

- (NSArray *)array:(NSString *)name
           ofClass:(Class<JSONDeserializable>)cls
          fromJSON:(NSDictionary<NSString *, id> *)json;

- (NSURL *)nullableURL:(NSString *)name
              fromJSON:(NSDictionary<NSString *, id> *)json;

- (NSDate *)date:(NSString *)name
        fromJSON:(NSDictionary<NSString *, id> *)json;

- (NSString *)string:(NSString *)name
            fromJSON:(NSDictionary<NSString *, id> *)json;

- (NSUInteger)unsignedInteger:(NSString *)name
                     fromJSON:(NSDictionary<NSString *, id> *)json;

- (NSURL *)url:(NSString *)name
      fromJSON:(NSDictionary<NSString *, id> *)json;

@end


NS_ASSUME_NONNULL_END
