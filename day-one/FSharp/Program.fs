open System
open System.IO

open FSharp.Data

type Entry = JsonProvider<"""1""">

let rec combinations acc size set =
    seq {
        match size, set with
        | n, x :: xs ->
            if n > 0
            then yield! combinations (x :: acc) (n - 1) xs

            if n >= 0 then yield! combinations acc n xs
        | 0, [] -> yield acc
        | _, [] -> ()
    }

[<EntryPoint>]
let main argv =
    let results =
        match argv with
        | [| filename; n; target |] ->
            File.ReadLines(filename)
            |> Seq.map Entry.Parse
            |> Seq.toList
            |> combinations [] (n |> int)
            |> Seq.filter (fun tup -> (target |> int) = List.sum tup)
            |> Some
        | _ -> None

    match results with
    | None -> printfn "No matches"
    | Some candidates ->
        Seq.head candidates
        |> Seq.reduce ((*))
        |> printfn "%d"
    // | Some candidates -> Seq.head candidates |> printfn "%A"

    0 // return an integer exit code
