using iot.Models;
using iot.Views;
using System;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Threading.Tasks;
using Xamarin.Forms;

using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.DataModel;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using System.Collections.Generic;
using System.Threading;


namespace iot.ViewModels
{
    public class SpotKey
    {
        public string location;
        public string spot; 
        
        public bool Equals(SpotKey other)
        {
            if (ReferenceEquals(null, other)) return false;
            if (ReferenceEquals(this, other)) return true;
            return other.location == location && other.spot == spot;
        }
        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != typeof(SpotKey)) return false;
            return Equals((SpotKey)obj);
        }
        public override int GetHashCode()
        {
            unchecked
            {
                int result = location.GetHashCode();
                result = (result * 397) ^ spot.GetHashCode();
                return result;
            }
        }
    }

    public class ItemsViewModel : BaseViewModel
    {
        private Item _selectedItem;

        public Dictionary<SpotKey, Item> SpotLookup;

        public ObservableCollection<Item> Items { get; }
        public Command LoadItemsCommand { get; }
        public Command<Item> ItemTapped { get; }

        private string _accessKey = "INSERT_KEY_HERE";
        private string _secretId = "INSERT_ID_HERE";

        private AmazonDynamoDBClient _client;
        private AmazonDynamoDBStreamsClient _streamClient;

        private DynamoDBContext _context;
        private AWSCredentials _credentials;

        private Timer _timerHandle;

        async public Task<List<Item>> UpdateSpots(string tableName)
        {
            var request = new ScanRequest
            {
                TableName = tableName
            };

            var response = await _client.ScanAsync(request);
            List<Item> added = new List<Item>();

            foreach (Dictionary<string, AttributeValue> tableItem in response.Items)
            {
                string location = "null";
                bool occupied = false;
                string spot = "null";
                string timeIn = "null";
                string billedTime = "null";

                foreach (KeyValuePair<string, AttributeValue> property in tableItem)
                {
                    if (property.Key == "Location")
                    {
                        location = property.Value.S;
                    }
                    else if (property.Key == "Occupied")
                    {
                        occupied = property.Value.BOOL;
                    }
                    else if (property.Key == "Spot")
                    {
                        spot = property.Value.N;
                    }
                    else if (property.Key == "TimeIn")
                    {
                        timeIn = property.Value.S;
                    }
                    else if (property.Key == "BilledTime")
                    {
                        billedTime = property.Value.S;
                    }
                }

                SpotKey key = new SpotKey()
                {
                    location = location,
                    spot = spot
                };

                if (SpotLookup.ContainsKey(key))
                {
                    SpotLookup[key].Location    = location;
                    SpotLookup[key].Spot        = spot;
                    SpotLookup[key].Occupied    = occupied;
                    SpotLookup[key].TimeIn      = timeIn;
                    SpotLookup[key].BilledTime  = billedTime;
                }
                else
                {
                    Item item = new Item()
                    {
                        Location = location,
                        Occupied = occupied,
                        Spot     = spot,
                        TimeIn   = timeIn,
                        BilledTime = billedTime,
                    };
                    added.Add(item);
                    SpotLookup.Add(key, item);
                }

            }

            return added;
        }

        async public void UpdateGarageTable(Object state)
        {
            await ExecuteLoadItemsCommand(false);
        }

        public void DisplayGarageInfo(ScanResponse result)
        {
        }

        public void HandleStream(object o, ResponseEventArgs r)
        {
            Console.WriteLine("Got a stream response");
        }


        public ItemsViewModel()
        {
            _credentials = new BasicAWSCredentials(_accessKey, _secretId);
            _client = new AmazonDynamoDBClient(_credentials, Amazon.RegionEndpoint.USEast2);
            _context = new DynamoDBContext(_client);

            SpotLookup = new Dictionary<SpotKey, Item>();

            Title = "Browse";
            Items = new ObservableCollection<Item>();
            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());

            ItemTapped = new Command<Item>(OnItemSelected);

            /*
            _streamClient = new AmazonDynamoDBStreamsClient(_credentials, Amazon.RegionEndpoint.USEast2);
            _streamClient.AfterResponseEvent += HandleStream;
            Task<ListStreamsResponse> listStreamsResponseTask = _streamClient.ListStreamsAsync();
            listStreamsResponseTask.Wait();
            ListStreamsResponse listStreamsResponse = listStreamsResponseTask.Result;


            foreach (StreamSummary streamSummary in listStreamsResponse.Streams)
            {
                int i = 0;
                i++;
            }
            */

            TimerCallback timerDelegate = new TimerCallback(UpdateGarageTable);
            _timerHandle = new Timer(timerDelegate, null, 1000, 1000);
        }

        async Task ExecuteLoadItemsCommand(bool showBusy=true)
        {
            if (showBusy)
            {
                IsBusy = true;
            }

            try
            {
                List<Item> added = await UpdateSpots("Smart_Park");

                if (added.Count > 0)
                {
                    foreach (var item in added)
                    {
                        Items.Add(item);
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
            }
            finally
            {
                IsBusy = false;
            }
        }

        public void OnAppearing()
        {
            IsBusy = true;
            SelectedItem = null;
        }

        public Item SelectedItem
        {
            get => _selectedItem;
            set
            {
                SetProperty(ref _selectedItem, value);
                OnItemSelected(value);
            }
        }

        async void OnItemSelected(Item item)
        {
            if (item == null)
                return;

            // This will push the ItemDetailPage onto the navigation stack
            await Shell.Current.GoToAsync($"{nameof(ItemDetailPage)}?{nameof(ItemDetailViewModel.ItemId)}={item.Spot}");
        }
    }
}