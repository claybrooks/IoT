using System;
using System.Windows.Input;
using Xamarin.Essentials;
using Xamarin.Forms;

using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.DataModel;
using Amazon.DynamoDBv2.Model;
using System.Collections.Generic;

namespace iot.ViewModels
{
    public class AboutViewModel : BaseViewModel
    {
        private string _accessKey = "";
        private string _secretId = "";

        private AmazonDynamoDBClient _client;
        private DynamoDBContext _context;

        public AboutViewModel()
        {
            Title = "About";
            OpenWebCommand = new Command(async () => await Browser.OpenAsync("https://aka.ms/xamarin-quickstart"));

            _client = new AmazonDynamoDBClient(_accessKey, _secretId, Amazon.RegionEndpoint.USEast2);
            _context = new DynamoDBContext(_client);

            var request = new ScanRequest
            {
                TableName = "Smart_Park"
            };

            var response = _client.ScanAsync(request);
            response.Wait();
            var result = response.Result;
        }

        public ICommand OpenWebCommand { get; }
    }
}