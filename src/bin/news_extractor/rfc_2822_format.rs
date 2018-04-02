use chrono::DateTime;
use chrono::Utc;
use serde;
use serde::Deserialize;
use serde::Deserializer;
use serde::Serializer;


pub fn serialize<S>(date: &DateTime<Utc>, serializer: S) -> Result<S::Ok, S::Error>
    where S: Serializer
{
    serializer.serialize_str(&date.to_rfc2822())
}

pub fn deserialize<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
    where D: Deserializer<'de>
{
    let string = String::deserialize(deserializer)?;
    match DateTime::parse_from_rfc2822(&string) {
        Ok(datetime) => Ok(datetime.with_timezone(&Utc)),
        Err(error) => Err(serde::de::Error::custom(error)),
    }
}
