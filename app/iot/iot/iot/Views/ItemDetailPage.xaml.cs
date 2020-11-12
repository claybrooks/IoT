using iot.ViewModels;
using System.ComponentModel;
using Xamarin.Forms;

namespace iot.Views
{
    public partial class ItemDetailPage : ContentPage
    {
        public ItemDetailPage()
        {
            InitializeComponent();
            BindingContext = new ItemDetailViewModel();
        }
    }
}