const inputFile = Deno.args[0]
const n = parseInt(Deno.args[1])
const target = parseInt(Deno.args[2])

const decoder = new TextDecoder("utf-8")
const dataString = decoder.decode(await Deno.readFile(inputFile))
const data: number[] = dataString.split("\n").map(l => JSON.parse(l))

function* combinations<T>(arr: T[], n: number) {
    function* _combinations<T>(a: T[], m: number): Generator<T[], undefined, undefined> {
        if (m == 1) {
            for (const val of a) {
                yield [val]
            }
        }
        else {
            const lineSets = a.map((line, index) =>
                Array.from(_combinations(a.slice(index + 1), m - 1))
                    .map((subline) => [line, ...subline]))
            for (const lineSet of lineSets) {
                for (const line of lineSet) {
                    yield line
                }
            }
        }
        return
    }
    for (const candidate of _combinations(arr, n)) {
        yield candidate
    }
}

function dayOne(data: number[], n: number, target: number) {
    for (const candidate of combinations(data, n)) {
        if (candidate.reduce((p, n) => p + n, 0) == target) {
            console.log(candidate)
            console.log(candidate.reduce((p, n) => p * n, 1))
            return
        }
    }
}

dayOne(data, n, target)
