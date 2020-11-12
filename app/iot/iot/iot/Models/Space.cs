using System;
using System.Collections.Generic;
using System.Text;

using Amazon.DynamoDBv2.DataModel;

namespace iot.Models
{
    [DynamoDBTable("Smart_Park")]
    class Space
    {
        public string location;
        public string spot;
        public bool occupied;
    }
}
