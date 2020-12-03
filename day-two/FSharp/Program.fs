// Learn more about F# at http://docs.microsoft.com/dotnet/fsharp

open System
open System.IO
open System.Text.RegularExpressions

let isValid minimumS maximumS (pattern: string) (candidate : string) =
    let minimum = minimumS |> int
    let maximum = maximumS |> int
    let patternRegex = Regex(pattern)
    let count = patternRegex.Matches(candidate).Count
    minimum <= count && count <= maximum

let isValidTwo p1S p2S (pattern: string) (candidate : string) =
    let p1 = -1 + (p1S |> int)
    let p2 = -1 + (p2S |> int)
    let patternLength = pattern.Length
    (
        (
            (candidate.Substring(p1, patternLength) = pattern) ||
            (candidate.Substring(p2, patternLength) = pattern)
        )
        && not (
            (candidate.Substring(p1, patternLength) = pattern) && (candidate.Substring(p2, patternLength) = pattern)
        )
    )

let deconstructMatch ( regexMatch : Match ) =
    let groups: GroupCollection = regexMatch.Groups
    let minimum = groups.["minimum"].Value
    let maximum = groups.["maximum"].Value
    let pattern = groups.["pattern"].Value
    let candidate = groups.["candidate"].Value
    (minimum, maximum, pattern, candidate )

[<EntryPoint>]
let main argv =
    let filename = match argv with
    | [| filename |] -> filename

    let rawEntries = File.ReadLines(filename)
    let pattern = "(?<minimum>\\d+)-(?<maximum>\\d+) (?<pattern>.): (?<candidate>.+)"
    let regex = Regex(pattern)
    let entries = Seq.map ((fun e -> (regex.Match e)) >> deconstructMatch) rawEntries

    let validities = Seq.map (fun e -> match e with | (a,b,c,d) -> isValid a b c d) entries
    let count = Seq.filter id validities |> List.ofSeq |> List.length
    printfn "%d" count
    
    let validities2 = Seq.map (fun e -> match e with | (a,b,c,d) -> isValidTwo a b c d) entries
    let count2 = Seq.filter id validities2 |> List.ofSeq |> List.length
    printfn "%d" count2

    0 // return an integer exit code