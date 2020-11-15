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

        private string _TimeIn = "";
        public string TimeIn
        {
            get { return _TimeIn; }
            set { _TimeIn = value; OnPropertyChanged("TimeIn"); }
        }

        private string _BilledTime = "";
        public string BilledTime
        {
            get { return _BilledTime; }
            set { _BilledTime = value; OnPropertyChanged("BilledTime"); }
        }
    }
}