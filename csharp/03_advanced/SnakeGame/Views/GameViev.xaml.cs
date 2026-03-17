using System.Windows.Controls;
using System.Windows.Input;

namespace SnakeGame.Views
{
    public partial class GameView : UserControl
    {
        public GameView()
        {
            InitializeComponent();
        }

        private void UserControl_KeyDown(object sender, KeyEventArgs e)
        {
            var viewModel = DataContext as ViewModels.GameViewModel;
            if (viewModel == null) return;

            switch (e.Key)
            {
                case Key.Up:
                case Key.W:
                    viewModel.MoveCommand.Execute("Up");
                    break;
                case Key.Down:
                case Key.S:
                    viewModel.MoveCommand.Execute("Down");
                    break;
                case Key.Left:
                case Key.A:
                    viewModel.MoveCommand.Execute("Left");
                    break;
                case Key.Right:
                case.Key.D:
                    viewModel.MoveCommand.Execute("Right");
                    break;
                case Key.Space:
                    viewModel.PauseCommand.Execute(null);
                    break;
            }
        }
    }
}
