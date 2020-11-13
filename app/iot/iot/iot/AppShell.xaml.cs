using iot.ViewModels;
using iot.Views;
using System;
using System.Collections.Generic;
using Xamarin.Forms;

namespace iot
{
    public partial class AppShell : Xamarin.Forms.Shell
    {
        public AppShell()
        {
            InitializeComponent();
            Routing.RegisterRoute(nameof(ItemDetailPage), typeof(ItemDetailPage));
        }

    }
}
