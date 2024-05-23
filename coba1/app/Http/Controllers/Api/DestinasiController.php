<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\DestinasiResource;
use App\Models\Destinasi;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class DestinasiController extends Controller
{
    /**
     * index
     *
     * @return void
     */
    public function index()
    {
        //get all posts
        $destinasi = Destinasi::latest()->paginate(5);

        //return collection of posts as a resource
        return $destinasi;
    }

    /**
     * store
     *
     * @param  mixed $request
     * @return void
     */
    public function store(Request $request)
    {
        //define validation rules
        $validator = Validator::make($request->all(), [
            'image'              => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
            'nama_destinasi'     => 'required',
            'tour'               => 'required',
            'harga'              => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //upload image
        $image = $request->file('image');
        $image->storeAs('public/posts', $image->hashName());

        //create post
        $destinasi = Destinasi::create([
            'image'              => $image->hashName(),
            'nama_destinasi'     => $request->nama_destinasi,
            'tour'               => $request->tour,
            'harga'              => $request->harga,
        ]);

        //return response
        return new DestinasiResource(true, 'Data Post Berhasil Ditambahkan!', $destinasi);
    }

    /**
     * show
     *
     * @param  mixed $id
     * @return void
     */
    public function show($id)
    {
        //find post by ID
        $destinasi = Destinasi::find($id);

        //return single post as a resource
        return new DestinasiResource(true, 'Detail Data Post!', $destinasi);
    }

    /**
     * update
     *
     * @param  mixed $request
     * @param  mixed $id
     * @return void
     */
    public function update(Request $request, $id)
    {
        //define validation rules
        $validator = Validator::make($request->all(), [
            'nama_destinasi'     => 'required',
            'tour'               => 'required',
            'harga'              => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //find post by ID
        $destinasi = Destinasi::find($id);

        //check if image is not empty
        if ($request->hasFile('image')) {

            //upload image
            $image = $request->file('image');
            $image->storeAs('public/posts', $image->hashName());

            //delete old image
            Storage::delete('public/posts/' . basename($destinasi->image));

            //update post with new image
            $destinasi->update([
                'image'              => $image->hashName(),
                'nama_destinasi'     => $request->nama_destinasi,
                'tour'               => $request->tour,
                'harga'              => $request->harga,
            ]);
        } else {

            //update post without image
            $destinasi->update([
                'nama_destinasi'     => $request->nama_destinasi,
                'tour'               => $request->tour,
                'harga'              => $request->harga,
            ]);
        }

        //return response
        return new DestinasiResource(true, 'Data Post Berhasil Diubah!', $destinasi);
    }

    /**
     * destroy
     *
     * @param  mixed $id
     * @return void
     */
    public function destroy($id)
    {

        //find post by ID
        $destinasi = Destinasi::find($id);

        //delete image
        Storage::delete('public/posts/'.basename($destinasi->image));

        //delete post
        $destinasi->delete();

        //return response
        return new DestinasiResource(true, 'Data Post Berhasil Dihapus!', null);
    }
}
