using System;
using System.ComponentModel;

namespace iot.Models
{
    public class Item : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }

        }

        private string _Location = "";
        public string Location 
        { 
            get { return _Location; }
            set { _Location = value; OnPropertyChanged("Location"); }
        }

        private string _Spot = "";
        public string Spot
        {
            get { return _Spot; }
            set { _Spot = value; OnPropertyChanged("Spot"); }
        }

        private bool _Occupied = false;
        public bool Occupied
        {
            get { return _Occupied; }
            set { _Occupied = value; OnPropertyChanged("Occupied"); }
        }
    }
}