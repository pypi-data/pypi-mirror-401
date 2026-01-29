use clap::Parser;
use hivemind_p2p::cli::{Cli, Command};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Command::Share(args) => {
            hivemind_p2p::output::init_logging(args.common.verbose);
            hivemind_p2p::hub::handle_share(args).await
        }
        Command::Join(args) => {
            hivemind_p2p::output::init_logging(args.common.verbose);
            hivemind_p2p::peer::handle_join(args).await
        }
    }
}
