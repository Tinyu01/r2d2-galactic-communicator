import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
import time
import json

from .galactic_morse import GalacticMorse, InvalidCharacterError, InvalidMorseCodeError

# Initialize Rich console for beautiful output
console = Console()

# R2-D2 ASCII Art
R2D2_ASCII = """
    [bold blue]
     ,---.
    /     \\
   | o   o |
   |   >   |
   |  ---  |
    \\     /
     `---'
      | |
     /   \\
    [R2-D2]
    [/bold blue]
"""

REBEL_BANNER = """
[bold red]╔══════════════════════════════════════════════════════════════╗[/bold red]
[bold red]║[/bold red] [bold white]🤖 R2-D2 GALACTIC COMMUNICATOR - REBEL TERMINAL[/bold white]      [bold red]║[/bold red]
[bold red]║[/bold red] [italic]Decoding Imperial Secrets with Pythonic Precision[/italic]    [bold red]║[/bold red]
[bold red]╚══════════════════════════════════════════════════════════════╝[/bold red]
"""

def display_startup():
    """Display the rebel startup sequence."""
    console.print(REBEL_BANNER)
    console.print(R2D2_ASCII, justify="center")
    
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Initializing hyperspace communication array...", total=None)
        time.sleep(1.5)
        progress.update(task, description="[green]✅ Ready for transmission!")
        time.sleep(0.5)
    
    console.print("\n[bold green]🟢 All systems operational. Awaiting your orders, Commander.[/bold green]")
    console.print("[dim]Use 'morse-cli --help' for mission briefing.[/dim]\n")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    🤖 R2-D2 Galactic Communicator - Your trusted astromech droid for covert communications.
    
    Translate between text and Morse code with the precision of a Jedi and the reliability of R2-D2.
    """
    if ctx.invoked_subcommand is None:
        display_startup()


@cli.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Encode text from file')
@click.option('--output', '-o', type=click.Path(), help='Save encoded message to file')
@click.option('--word-space', default='/', help='Word separator (default: /)')
@click.option('--char-space', default=' ', help='Character separator (default: space)')
@click.option('--quiet', '-q', is_flag=True, help='Suppress R2-D2 chatter')
def encode(text: Optional[str], file: Optional[str], output: Optional[str], 
           word_space: str, char_space: str, quiet: bool):
    """
    🔵 Encode text into Morse code for secret Rebel transmissions.
    
    Examples:
        morse-cli encode "Help me Obi-Wan"
        morse-cli encode --file rebel_message.txt
        morse-cli encode "SOS" --output distress_signal.morse
    """
    if not quiet:
        console.print("\n[bold blue]🔵 ENCODING MODE: Text → Morse Code[/bold blue]")
    
    r2d2 = GalacticMorse()
    
    # Get input text
    if file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                input_text = f.read().strip()
            if not quiet:
                console.print(f"[dim]📁 Reading from: {file}[/dim]")
        except Exception as e:
            console.print(f"[bold red]❌ File error: {e}[/bold red]")
            sys.exit(1)
    elif text:
        input_text = text
    else:
        # Read from stdin
        try:
            input_text = sys.stdin.read().strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Transmission interrupted by user.[/yellow]")
            sys.exit(0)
    
    if not input_text:
        console.print("[bold red]❌ No input text provided.[/bold red]")
        sys.exit(1)
    
    # Perform encoding
    try:
        with Progress(
            SpinnerColumn("arrow3"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            if not quiet:
                task = progress.add_task("[cyan]🚀 Encoding through hyperspace...", total=None)
                time.sleep(0.8)
            
            morse_code = r2d2.text_to_morse(input_text, word_space, char_space)
            
            if not quiet:
                progress.update(task, description="[green]✅ Encoding complete!")
                time.sleep(0.3)
        
        # Display results
        if not quiet:
            result_table = Table(show_header=True, header_style="bold magenta")
            result_table.add_column("Type", style="cyan", width=12)
            result_table.add_column("Content", style="white")
            
            result_table.add_row("📝 Original", input_text[:100] + "..." if len(input_text) > 100 else input_text)
            result_table.add_row("📡 Morse Code", morse_code)
            
            console.print(result_table)
            console.print(f"\n[green]✅ Successfully encoded {len(input_text)} characters into Morse code.[/green]")
        else:
            console.print(morse_code)
        
        # Save to file if requested
        if output:
            try:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(morse_code)
                if not quiet:
                    console.print(f"[green]💾 Saved to: {output}[/green]")
            except Exception as e:
                console.print(f"[bold red]❌ Save error: {e}[/bold red]")
                sys.exit(1)
    
    except InvalidCharacterError as e:
        console.print(f"\n[bold red]🚨 IMPERIAL INTERFERENCE DETECTED![/bold red]")
        console.print(f"[red]{e}[/red]")
        console.print("[dim]Tip: Use only A-Z, 0-9, punctuation, and supported emojis (⚡🚀🌟🤖⭐🔥)[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('morse_code', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Decode Morse code from file')
@click.option('--output', '-o', type=click.Path(), help='Save decoded message to file')
@click.option('--strict', is_flag=True, help='Strict mode: fail on invalid patterns')
@click.option('--quiet', '-q', is_flag=True, help='Suppress R2-D2 chatter')
def decode(morse_code: Optional[str], file: Optional[str], output: Optional[str], 
           strict: bool, quiet: bool):
    """
    🔴 Decode Morse code into readable text for Rebel intelligence.
    
    Examples:
        morse-cli decode "... --- ..."
        morse-cli decode --file intercepted.morse
        morse-cli decode ".- -..." --strict
    """
    if not quiet:
        console.print("\n[bold red]🔴 DECODING MODE: Morse Code → Text[/bold red]")
    
    r2d2 = GalacticMorse()
    
    # Get input morse code
    if file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                input_morse = f.read().strip()
            if not quiet:
                console.print(f"[dim]📁 Reading from: {file}[/dim]")
        except Exception as e:
            console.print(f"[bold red]❌ File error: {e}[/bold red]")
            sys.exit(1)
    elif morse_code:
        input_morse = morse_code
    else:
        # Read from stdin
        try:
            input_morse = sys.stdin.read().strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Transmission interrupted by user.[/yellow]")
            sys.exit(0)
    
    if not input_morse:
        console.print("[bold red]❌ No Morse code provided.[/bold red]")
        sys.exit(1)
    
    # Validate morse code
    is_valid, error_msg = r2d2.validate_morse_code(input_morse)
    if not is_valid and not quiet:
        console.print(f"[yellow]⚠️  Warning: {error_msg}[/yellow]")
    
    # Perform decoding
    try:
        with Progress(
            SpinnerColumn("arrow3"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            if not quiet:
                task = progress.add_task("[cyan]🔍 Analyzing Rebel transmission...", total=None)
                time.sleep(0.8)
            
            decoded_text = r2d2.morse_to_text(input_morse, strict)
            
            if not quiet:
                progress.update(task, description="[green]✅ Decoding complete!")
                time.sleep(0.3)
        
        # Display results
        if not quiet:
            result_table = Table(show_header=True, header_style="bold magenta")
            result_table.add_column("Type", style="cyan", width=12)
            result_table.add_column("Content", style="white")
            
            result_table.add_row("📡 Morse Code", input_morse[:100] + "..." if len(input_morse) > 100 else input_morse)
            result_table.add_row("📝 Decoded", decoded_text)
            
            console.print(result_table)
            console.print(f"\n[green]✅ Successfully decoded Morse transmission.[/green]")
            
            if '?' in decoded_text:
                console.print("[yellow]⚠️  Some characters could not be decoded (marked with ?).[/yellow]")
        else:
            console.print(decoded_text)
        
        # Save to file if requested
        if output:
            try:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(decoded_text)
                if not quiet:
                    console.print(f"[green]💾 Saved to: {output}[/green]")
            except Exception as e:
                console.print(f"[bold red]❌ Save error: {e}[/bold red]")
                sys.exit(1)
    
    except InvalidMorseCodeError as e:
        console.print(f"\n[bold red]🚨 DARK SIDE CORRUPTION DETECTED![/bold red]")
        console.print(f"[red]{e}[/red]")
        console.print("[dim]Tip: Use only dots (.), dashes (-), spaces, and word separators (/)[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
def chars(format):
    """
    📋 Display the Galactic Code Archive (supported character mappings).
    """
    console.print("\n[bold cyan]📋 GALACTIC CODE ARCHIVE[/bold cyan]")
    console.print("[dim]All supported characters and their Morse code equivalents[/dim]\n")
    
    r2d2 = GalacticMorse()
    mappings = r2d2.get_supported_characters()
    
    if format == 'table':
        # Group by category for better display
        categories = {
            'Letters': {k: v for k, v in mappings.items() if k.isalpha()},
            'Numbers': {k: v for k, v in mappings.items() if k.isdigit()},
            'Punctuation': {k: v for k, v in mappings.items() if not k.isalnum() and k not in ['⚡', '🚀', '🌟', '🤖', '⭐', '🔥', ' ']},
            'Star Wars Emojis': {k: v for k, v in mappings.items() if k in ['⚡', '🚀', '🌟', '🤖', '⭐', '🔥']}
        }
        
        for category, chars in categories.items():
            if chars:
                table = Table(title=f"[bold]{category}[/bold]", show_header=True, header_style="bold blue")
                table.add_column("Character", style="cyan", width=12)
                table.add_column("Morse Code", style="yellow")
                table.add_column("Description", style="dim")
                
                descriptions = {
                    '⚡': 'Force Lightning',
                    '🚀': 'X-Wing Fighter',
                    '🌟': 'Death Star',
                    '🤖': 'R2-D2',
                    '⭐': 'Imperial Symbol',
                    '🔥': 'Lightsaber',
                    ' ': 'Word separator'
                }
                
                for char, morse in sorted(chars.items()):
                    desc = descriptions.get(char, '')
                    table.add_row(char, morse, desc)
                
                console.print(table)
                console.print()
    
    else:  # JSON format
        console.print(json.dumps(mappings, indent=2, ensure_ascii=False))
    
    console.print(f"[green]✅ Total supported characters: {len(mappings)}[/green]")


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--direction', type=click.Choice(['encode', 'decode']), required=True, help='Translation direction')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def batch(input_file: str, direction: str, output: Optional[str]):
    """
    📦 Process multiple messages in batch mode for large-scale Rebel operations.
    
    Input file should contain one message per line.
    """
    console.print(f"\n[bold purple]📦 BATCH MODE: Processing {direction} operations[/bold purple]")
    
    r2d2 = GalacticMorse()
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        console.print(f"[bold red]❌ File error: {e}[/bold red]")
        sys.exit(1)
    
    if not lines:
        console.print("[bold red]❌ No valid input lines found.[/bold red]")
        sys.exit(1)
    
    console.print(f"[dim]📁 Processing {len(lines)} lines from: {input_file}[/dim]")
    
    # Process batch
    to_morse = direction == 'encode'
    results = r2d2.batch_translate(lines, to_morse)
    
    # Display results
    success_count = sum(1 for r in results if r['success'])
    error_count = len(results) - success_count
    
    result_table = Table(show_header=True, header_style="bold magenta")
    result_table.add_column("#", style="dim", width=4)
    result_table.add_column("Input", style="cyan", width=30)
    result_table.add_column("Output", style="yellow", width=30)
    result_table.add_column("Status", style="white", width=10)
    
    for result in results[:10]:  # Show first 10 results
        status = "✅ OK" if result['success'] else "❌ Error"
        input_text = result['input'][:27] + "..." if len(result['input']) > 30 else result['input']
        output_text = result['output'][:27] + "..." if result['output'] and len(result['output']) > 30 else (result['output'] or "N/A")
        
        result_table.add_row(
            str(result['index'] + 1),
            input_text,
            output_text,
            status
        )
    
    console.print(result_table)
    
    if len(results) > 10:
        console.print(f"[dim]... and {len(results) - 10} more results[/dim]")
    
    # Show summary
    console.print(f"\n[bold]📊 BATCH SUMMARY:[/bold]")
    console.print(f"[green]✅ Successful: {success_count}[/green]")
    console.print(f"[red]❌ Failed: {error_count}[/red]")
    console.print(f"[blue]📈 Success Rate: {success_count/len(results)*100:.1f}%[/blue]")
    
    # Save results if requested
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                for result in results:
                    if result['success']:
                        f.write(f"{result['output']}\n")
                    else:
                        f.write(f"ERROR: {result['error']}\n")
            console.print(f"[green]💾 Results saved to: {output}[/green]")
        except Exception as e:
            console.print(f"[bold red]❌ Save error: {e}[/bold red]")


if __name__ == "__main__":
    cli()