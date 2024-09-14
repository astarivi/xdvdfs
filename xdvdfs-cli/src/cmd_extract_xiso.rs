use crate::cmd_pack::PackArgs;
use crate::cmd_read::TreeArgs;
use crate::cmd_unpack::UnpackArgs;
use crate::{cmd_pack, cmd_read, cmd_unpack};
use clap::{ArgGroup, Args};
use maybe_async::maybe_async;

#[derive(Args)]
#[command(about = "Enable extract-xiso compatibility mode")]
#[command(group(
    ArgGroup::new("mode")
        .args(&["create", "extract", "list"])
))]
pub struct ExtractXisoArgs {
    #[arg(
        short = 'x',
        help = "Extract xiso(s) (the default mode if none is given)"
    )]
    extract: bool,

    #[arg(short = 'c', action, help = "Create an XISO from a directory")]
    create: bool,

    #[arg(short = 'l', help = "List files in xiso(s)")]
    list: bool,

    #[arg(short = 'd', value_name = "directory", value_parser = clap::value_parser!(String))]
    directory: Option<String>,

    #[arg(help = "Path to source directory or ISO image")]
    input_path: String,

    #[arg(help = "Path to output directory or ISO image")]
    output_path: Option<String>,
}

#[maybe_async]
pub async fn cmd_extract_xiso(args: &ExtractXisoArgs) -> Result<(), anyhow::Error> {
    if args.create {
        let create_args = PackArgs {
            source_path: args.input_path.clone(),
            image_path: args.output_path.clone(),
        };

        cmd_pack::cmd_pack(&create_args).await?;
    } else if args.list {
        let tree_args = TreeArgs {
            image_path: args.input_path.clone(),
        };

        cmd_read::cmd_tree(&tree_args).await?;
    } else {
        let unpack_args = UnpackArgs {
            image_path: args.input_path.clone(),
            path: args.directory.clone(),
        };

        cmd_unpack::cmd_unpack(&unpack_args).await?;
    }

    Ok(())
}
