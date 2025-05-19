import Head from 'next/head'
import FileUpload from '../components/FileUpload'

export default function Home() {
  return (
    <>
      <Head>
        <title>GoldenRecord - Entity Matching Tool</title>
      </Head>
      <main className="min-h-screen bg-gray-100 py-10">
        <h1 className="text-center text-3xl font-bold text-gray-800 mb-6">
          GoldenRecord – Entity Matching Tool
        </h1>
        <FileUpload />
      </main>
    </>
  )
}
